from arena_missions.challenges.ambiguous_pickup import register_ambiguous_pickup_challenges
from arena_missions.challenges.breaking_things import register_breaking_things_challenges
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
from arena_missions.challenges.pickup_from_printer import register_pickup_from_printer_challenges
from arena_missions.challenges.pickup_stack import register_pickup_plate_stack_challenges
from arena_missions.challenges.place_stack import (
    register_place_bowl_stack_from_gravity_pad,
    register_place_plate_stack_challenges,
)
from arena_missions.challenges.using_coffee_unmaker import register_coffee_unmaker_challenges
from arena_missions.challenges.using_color_changer import register_color_changer_challenges


def load_challenges() -> None:
    """Run all the register functions to load the challenges."""
    register_repair_broken_things(enable_color_variants=False)
    register_objects_with_fridge_challenges()
    register_objects_with_freezer_challenges()
    register_warehouse_cabinet_challenges(enable_color_variants=False)
    register_fill_objects_in_sink(enable_color_variants=False)
    register_carrot_maker_challenges(enable_color_variants=False)
    register_clean_dirty_plates(enable_color_variants=False)
    register_coffee_unmaker_challenges(enable_color_variants=False)
    register_heat_things(enable_color_variants=False)
    register_color_changer_challenges()
    register_print_things()
    register_repair_carrots(enable_color_variants=False)

    register_pickup_plate_stack_challenges(enable_color_variants=False)
    register_place_plate_stack_challenges(enable_color_variants=False)
    register_ambiguous_pickup_challenges()
    register_pickup_from_printer_challenges()
    register_breaking_things_challenges(enable_color_variants=False)
    register_place_bowl_stack_from_gravity_pad(enable_color_variants=True)
