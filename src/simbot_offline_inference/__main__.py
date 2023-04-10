import typer

from simbot_offline_inference.commands import (
    generate_trajectories,
    print_high_level_keys,
    run_background_services,
    run_their_evaluation,
    validate_cdfs,
    validate_generated_missions,
)


app = typer.Typer(name="Run inference offline.", no_args_is_help=True, add_completion=False)


app.command(rich_help_panel="Run")(run_background_services)

app.command(rich_help_panel="Preparation")(validate_cdfs)
app.command(rich_help_panel="Preparation")(validate_generated_missions)
app.command(rich_help_panel="Preparation")(print_high_level_keys)

app.command(rich_help_panel="Generation")(generate_trajectories)

app.command(rich_help_panel="Evaluation")(run_their_evaluation)


if __name__ == "__main__":
    app()
