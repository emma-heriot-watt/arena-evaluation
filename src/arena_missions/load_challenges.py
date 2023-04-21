from arena_missions.challenges.clean_dirty_plate import register_clean_dirty_plates
from arena_missions.challenges.fill_object_in_sink import register_fill_objects_in_sink
from arena_missions.challenges.objects_in_containers import (
    register_objects_with_freezer_challenges,
    register_objects_with_fridge_challenges,
    register_warehouse_cabinet_challenges,
)
from arena_missions.challenges.operate_carrot_maker import register_carrot_maker_challenges
from arena_missions.challenges.operate_microwave import register_heat_things
from arena_missions.challenges.operate_printer import register_print_things
from arena_missions.challenges.operate_time_machine import (
    register_repair_broken_things,
    register_repair_carrots,
)
from arena_missions.challenges.pickup_stack import register_plate_stack_challenges
from arena_missions.challenges.using_coffee_unmaker import register_coffee_unmaker_challenges
from arena_missions.challenges.using_color_changer import register_color_changer_challenges


def load_challenges() -> None:
    """Run all the register functions to load the challenges."""
    register_repair_broken_things()
    register_objects_with_fridge_challenges()
    register_objects_with_freezer_challenges()
    register_warehouse_cabinet_challenges()
    register_fill_objects_in_sink()
    register_carrot_maker_challenges()
    register_clean_dirty_plates()
    register_coffee_unmaker_challenges()
    register_heat_things()
    register_color_changer_challenges()
    register_print_things()
    register_repair_carrots()

    register_plate_stack_challenges()
