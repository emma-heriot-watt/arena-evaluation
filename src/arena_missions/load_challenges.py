from arena_missions.challenges.clean_dirty_plate import register_clean_dirty_plates
from arena_missions.challenges.fill_object_in_sink import register_fill_objects_in_sink
from arena_missions.challenges.objects_in_containers import (
    register_objects_with_freezer_challenges,
    register_objects_with_fridge_challenges,
)
from arena_missions.challenges.operate_time_machine import register_repair_broken_things
from arena_missions.challenges.using_coffee_unmaker import register_coffee_unmaker_challenges


def load_challenges() -> None:
    """Run all the register functions to load the challenges."""
    register_repair_broken_things()

    register_objects_with_fridge_challenges()
    register_objects_with_freezer_challenges()

    register_clean_dirty_plates()

    register_fill_objects_in_sink()
    register_coffee_unmaker_challenges()