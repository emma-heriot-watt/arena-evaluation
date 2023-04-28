from collections.abc import Iterator
from copy import deepcopy
from itertools import groupby
from typing import Any, Callable, Optional, Union

from deepmerge import always_merger
from pydantic import BaseModel, Field

from arena_missions.constants.arena import OfficeLayout, OfficeRoom
from arena_missions.structures import HighLevelKey, RequiredObject, StateCondition, TaskGoal


class ChallengeBuilderOutput(BaseModel):
    """Output of a challenge builder function."""

    start_room: OfficeRoom
    required_objects: dict[str, RequiredObject]
    plan: list[str]

    task_goals: list[TaskGoal]
    state_conditions: list[StateCondition] = Field(default_factory=list)

    preparation_plan: list[str] = Field(default_factory=list)

    # If you want to override the office layout, set this.
    office_layout: Optional[OfficeLayout] = None

    # Whether or not to include all the default objects like open doors, etc.
    # If you don't care, just ignore it.
    include_all_default_objects: Optional[bool] = True

    randomise_start_position: bool = True

    @property
    def required_objects_list(self) -> list[RequiredObject]:
        """Return a list of lists of required objects."""
        return list(self.required_objects.values())


ChallengeBuilderFunction = Callable[[], ChallengeBuilderOutput]


class ChallengeBuilder:
    """Registrable-style class that registers challenge builders to easily generate them."""

    _registry: list[tuple[HighLevelKey, ChallengeBuilderFunction]] = []

    def __iter__(self) -> Iterator[tuple[HighLevelKey, ChallengeBuilderFunction]]:
        """Iterate over the registry."""
        yield from self._registry

    @classmethod
    def register(
        cls, high_level_key: Union[str, HighLevelKey]
    ) -> Callable[[ChallengeBuilderFunction], ChallengeBuilderFunction]:
        """Register a challenge builder."""
        # mypy errors if we don't reassign the parsed high-level key to a new variable.
        # Either that is a bug, or it knows something we don't.
        parsed_high_level_key = (
            HighLevelKey.from_string(high_level_key)
            if isinstance(high_level_key, str)
            else high_level_key
        )

        def decorator(func: ChallengeBuilderFunction) -> ChallengeBuilderFunction:
            # Registry count before registering
            registry_count = len(ChallengeBuilder._registry)  # noqa: WPS437

            # Register the challenge builder
            ChallengeBuilder._registry.append((parsed_high_level_key, func))  # noqa: WPS437

            # Get the count after removing duplicates
            registry_count_after_duplicates_removed = len(
                set(ChallengeBuilder._registry)  # noqa: WPS437
            )

            # If the count is the same, then we didn't add a new challenge builder
            if registry_count == registry_count_after_duplicates_removed:
                raise ValueError(
                    f"Challenge builder already registered for: ({parsed_high_level_key}, {func})."
                )

            return func

        return decorator

    @classmethod
    def register_with_modifiers(
        cls,
        high_level_key: Union[str, HighLevelKey],
        modified_kwargs: dict[str, Any],
    ) -> Callable[[ChallengeBuilderFunction], ChallengeBuilderFunction]:
        """Register a challenge builder with modifiers."""

        def decorator(func: ChallengeBuilderFunction) -> ChallengeBuilderFunction:
            # Register the modified challenge builder
            ChallengeBuilder.register(high_level_key)(
                ChallengeBuilder.modify_challenge_builder_function_output(func, modified_kwargs)
            )

            return func

        return decorator

    @classmethod
    def count_available_functions_per_key(cls) -> dict[HighLevelKey, int]:
        """List all keys and how many functions connect with them."""
        key_counts: dict[HighLevelKey, int] = {}

        # Sort the registry by the high-level key
        sorted_registry = sorted(cls._registry, key=lambda x: x[0].key)

        for k, g in groupby(sorted_registry, key=lambda x: x[0]):
            key_counts[k] = len(list(g))

        return key_counts

    @classmethod
    def list_available(cls) -> list[HighLevelKey]:
        """List all available high-level keys."""
        return list({key for key, _ in cls._registry})

    @staticmethod
    def modify_challenge_builder_function_output(  # noqa: WPS602
        function: ChallengeBuilderFunction, modified_kwargs: dict[str, Any]
    ) -> ChallengeBuilderFunction:
        """Modify the output of a challenge builder function."""

        def wrapper() -> ChallengeBuilderOutput:
            # Call the original function
            output = function().dict(by_alias=True)
            output = deepcopy(output)
            # Modify the output
            always_merger.merge(output, modified_kwargs)
            # Return the modified output
            return ChallengeBuilderOutput.parse_obj(output)

        return wrapper
