# Offline Inference on the SimBot arena


## Installing dependencies

You can run the convenience script at `scripts/prepare-user-area.sh`. I **HIGHLY RECOMMEND** reading the script to know what it does, because you might not need all of it! 

## Running things

> **Note**
>
> If you need sudo to run Docker, prefix the `poetry run` command with: `sudo -E env PATH=$PATH`.

### T1 evaluation (the one for [evai.ai](https://eval.ai/web/challenges/challenge-page/1903/overview))

When running T1, progress is sent to [wandb.ai/emma-simbot/alexa-arena-evaluation](https://wandb.ai/emma-simbot/alexa-arena-evaluation). All session IDs are prefixed with `T1-`.

#### Steps

1. Create a new tmux session.
2. In one tmux pane, run `sudo /usr/bin/X :1 &`
3. In the other pane, run:

   ```bash
   poetry run python -m simbot_offline_inference run-background-services
   ```
4. Finally, in a third pane, run:

   ```bash
   poetry run python -m simbot_offline_inference run-their-evaluation T1
   ```
5. Let it run.

### Running the trajectory generation

When running trajectories, each one is a new "run", and all the runs are tracked at [wandb.ai/emma-simbot/arena-high-level-trajectories](https://wandb.ai/emma-simbot/arena-high-level-trajectories).

#### Steps

1. Create a new tmux session.
2. In one tmux pane, run `sudo /usr/bin/X :1 &`
3. In the other pane, run:

   ```bash
   poetry run python -m simbot_offline_inference run-background-services
   ```
4. Finally, in a third pane, run:

   ```bash
   poetry run python -m simbot_offline_inference generate-trajectories
   ```
5. Let it run.
