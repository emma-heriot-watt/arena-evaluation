import random
from collections.abc import Iterator
from typing import Optional, get_args

from arena_missions.builders.challenge_builder import (
    ChallengeBuilder,
    ChallengeBuilderFunction,
    ChallengeBuilderOutput,
)
from arena_missions.builders.required_objects_builder import RequiredObjectBuilder
from arena_missions.constants.arena import OfficeLayout
from arena_missions.structures import CDF, CDFScene, HighLevelKey, Mission, RequiredObject


class MissionBuilder:
    """Build missions for the Arena."""

    def __init__(
        self,
        challenge_builder: ChallengeBuilder,
        required_object_builder: RequiredObjectBuilder,
        unity_scene_rng_seed: Optional[int] = None,
    ) -> None:
        self.challenge_builder = challenge_builder
        self.required_object_builder = required_object_builder

        self._unity_scene_rng_seed = unity_scene_rng_seed

    @property
    def cdf_floor_plan(self) -> str:
        """Convert the Unity Scene RNG seed to a string for the `floor_plan`."""
        return str(self._unity_scene_rng_seed) if self._unity_scene_rng_seed is not None else "-1"

    def generate_all_missions(self) -> Iterator[Mission]:
        """Generate all missions."""
        yield from (
            self.generate_mission(high_level_key, challenge_builder_function)
            for high_level_key, challenge_builder_function in self.challenge_builder
        )

    def generate_mission(
        self, high_level_key: HighLevelKey, challenge_builder_function: ChallengeBuilderFunction
    ) -> Mission:
        """Generate a mission."""
        builder_output = challenge_builder_function()
        cdf = self.generate_cdf(builder_output)
        return Mission(
            high_level_key=high_level_key,
            plan=builder_output.plan,
            cdf=cdf,
            preparation_plan=builder_output.preparation_plan,
            randomise_start_position=builder_output.randomise_start_position,
        )

    def generate_cdf(self, challenge_builder_output: ChallengeBuilderOutput) -> CDF:
        """Generate a challenge."""
        required_objects = [
            *challenge_builder_output.required_objects_list,
            *self.generate_default_arena_objects_if_required(
                challenge_builder_output.include_all_default_objects
            ),
        ]

        cdf_scene = CDFScene(
            roomLocation=[challenge_builder_output.start_room],
            floor_plan=self.cdf_floor_plan,
            required_objects=required_objects,
            layoutOverride=self.generate_office_layout_if_required(
                challenge_builder_output.office_layout
            ),
        )
        return CDF(
            scene=cdf_scene,
            task_goals=challenge_builder_output.task_goals,
            stateconditions=challenge_builder_output.state_conditions,
        )

    def generate_default_arena_objects_if_required(
        self, include_all_default_objects: Optional[bool]
    ) -> list[RequiredObject]:
        """Generate default arena objects."""
        if include_all_default_objects is None:
            include_all_default_objects = random.choice([True, False])

        return (
            self.required_object_builder.default_objects() if include_all_default_objects else []
        )

    def generate_office_layout_if_required(
        self, office_layout: Optional[OfficeLayout]
    ) -> OfficeLayout:
        """Generate office layout."""
        return office_layout if office_layout else random.choice(get_args(OfficeLayout))
