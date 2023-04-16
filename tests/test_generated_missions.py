from deepdiff import DeepDiff
from pytest_cases import fixture, param_fixture

from arena_missions.builders import (
    ChallengeBuilder,
    ChallengeBuilderFunction,
    MissionBuilder,
    RequiredObjectBuilder,
)
from arena_missions.structures import CDF, HighLevelKey, Mission


@fixture(scope="module")
def required_object_builder() -> RequiredObjectBuilder:
    return RequiredObjectBuilder()


@fixture(scope="module")
def mission_builder(required_object_builder: RequiredObjectBuilder) -> MissionBuilder:
    return MissionBuilder(ChallengeBuilder(), required_object_builder)


challenge_builder_function = param_fixture(
    "challenge_builder_function",
    [x[1] for x in ChallengeBuilder()],
    ids=[x[0].key for x in ChallengeBuilder()],
    scope="module",
)

build_challenge_tuple = param_fixture(
    "build_challenge_tuple",
    list(ChallengeBuilder()),
    ids=[x[0].key for x in ChallengeBuilder()],
    scope="module",
)


def test_challenge_builder_instantiates_without_error() -> None:
    assert ChallengeBuilder()


def test_registered_challenge_builders_are_valid(
    challenge_builder_function: ChallengeBuilderFunction,
) -> None:
    builder_output = challenge_builder_function()
    assert builder_output


def test_generated_cdfs_are_valid(
    challenge_builder_function: ChallengeBuilderFunction,
    mission_builder: MissionBuilder,
) -> None:
    builder_output = challenge_builder_function()
    cdf = mission_builder.generate_cdf(builder_output)

    # Verify the CDF is valid
    assert cdf

    # Make sure the CDF can be reimported successfully
    reimported_cdf = CDF.parse_obj(cdf.dict(by_alias=True))
    assert reimported_cdf

    # Make sure the reimported CDF is identical to the original. If there is no difference, they
    # are identical.
    assert not DeepDiff(cdf.dict(by_alias=True), reimported_cdf.dict(by_alias=True))


def test_generated_missions_are_valid(
    build_challenge_tuple: tuple[HighLevelKey, ChallengeBuilderFunction],
    mission_builder: MissionBuilder,
) -> None:
    high_level_key, challenge_builder_function = build_challenge_tuple
    mission = mission_builder.generate_mission(high_level_key, challenge_builder_function)

    assert mission

    # Make sure the mission can be reimported successfully
    assert Mission.parse_obj(mission.dict(by_alias=True))
