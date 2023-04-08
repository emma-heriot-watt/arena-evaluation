from arena_missions.builders.challenge_builder import CHALLENGE_REGISTRY
from arena_missions.builders.mission_builder import MissionBuilder
from arena_missions.builders.required_objects_builder import RequiredObjectBuilder
from arena_missions.structures.cdf import CDF
from arena_missions.structures.mission import Mission


def test_every_challenge_built_is_valid() -> None:
    required_object_builder = RequiredObjectBuilder()

    for challenge_builder in CHALLENGE_REGISTRY.values():
        builder_output = challenge_builder(required_object_builder)
        assert builder_output


def test_every_mission_built_is_valid() -> None:
    required_object_builder = RequiredObjectBuilder()
    mission_builder = MissionBuilder(CHALLENGE_REGISTRY, required_object_builder)

    # temporarily monkey-patch the generate_plans method to avoid NotImplementedError
    mission_builder.generate_plans = lambda high_level_key: [["dummy_utterance"]]

    for mission in mission_builder.generate_all_missions():
        assert mission

        # Make sure the mission can be reimported successfully
        assert Mission.parse_obj(mission.dict(by_alias=True))

        # Make sure the CDF can be reimported successfully
        assert CDF.parse_obj(mission.cdf.dict(by_alias=True))
