from arena_missions.builders.challenge_builder import ChallengeBuilder
from arena_missions.builders.mission_builder import MissionBuilder
from arena_missions.builders.required_objects_builder import RequiredObjectBuilder
from arena_missions.structures.cdf import CDF
from arena_missions.structures.mission import Mission


def test_challenge_builder_loads_without_error() -> None:
    assert ChallengeBuilder()


def test_every_challenge_built_is_valid() -> None:
    required_object_builder = RequiredObjectBuilder()
    challenge_builder = ChallengeBuilder()

    for _, challenge_builder_function in challenge_builder:
        builder_output = challenge_builder_function(required_object_builder)
        assert builder_output


def test_every_mission_built_is_valid() -> None:
    required_object_builder = RequiredObjectBuilder()
    challenge_builder = ChallengeBuilder()
    mission_builder = MissionBuilder(challenge_builder, required_object_builder)

    for mission in mission_builder.generate_all_missions():
        assert mission

        # Make sure the mission can be reimported successfully
        assert Mission.parse_obj(mission.dict(by_alias=True))

        # Make sure the CDF can be reimported successfully
        assert CDF.parse_obj(mission.cdf.dict(by_alias=True))
