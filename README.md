<div align='center'>

# EMMA: Evaluation on the Alexa Arena

<a href="https://www.python.org/">
  <img alt="Python 3.9" src="https://img.shields.io/badge/-Python 3.9+-blue?logo=python&logoColor=white">
</a>
<a href="https://pytorch.org/">
  <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white">
</a>
<a href="https://python-poetry.org">
  <img alt="Poetry" src="https://img.shields.io/badge/Poetry-1E293B?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2aWV3Qm94PSIwIDAgNDQ4LjE3IDU2MCI+PGRlZnM+PHN0eWxlPi5jbHMtMXtpc29sYXRpb246aXNvbGF0ZTt9LmNscy0ye2ZpbGw6dXJsKCNyYWRpYWwtZ3JhZGllbnQpO30uY2xzLTN7ZmlsbDp1cmwoI3JhZGlhbC1ncmFkaWVudC0yKTt9LmNscy00LC5jbHMtNSwuY2xzLTZ7bWl4LWJsZW5kLW1vZGU6bXVsdGlwbHk7fS5jbHMtNHtmaWxsOnVybCgjbGluZWFyLWdyYWRpZW50KTt9LmNscy01e2ZpbGw6dXJsKCNsaW5lYXItZ3JhZGllbnQtMik7fS5jbHMtNntmaWxsOnVybCgjbGluZWFyLWdyYWRpZW50LTMpO30uY2xzLTd7bWl4LWJsZW5kLW1vZGU6c2NyZWVuO2ZpbGw6dXJsKCNyYWRpYWwtZ3JhZGllbnQtMyk7fTwvc3R5bGU+PHJhZGlhbEdyYWRpZW50IGlkPSJyYWRpYWwtZ3JhZGllbnQiIGN4PSI0MzguMyIgY3k9IjYzOS4wMSIgcj0iNTY5Ljk0IiBncmFkaWVudFRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM2ODc3ZWMiLz48c3RvcCBvZmZzZXQ9IjAuNiIgc3RvcC1jb2xvcj0iIzUzNjJjZiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzQzNTJiOSIvPjwvcmFkaWFsR3JhZGllbnQ+PHJhZGlhbEdyYWRpZW50IGlkPSJyYWRpYWwtZ3JhZGllbnQtMiIgY3g9IjY1LjY0IiBjeT0iLTE2LjIxIiByPSI3NDYuNDYiIGdyYWRpZW50VHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCAwKSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzAwZDVmZiIvPjxzdG9wIG9mZnNldD0iMC4zOCIgc3RvcC1jb2xvcj0iIzAwYjhlYiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzAwODBjNSIvPjwvcmFkaWFsR3JhZGllbnQ+PGxpbmVhckdyYWRpZW50IGlkPSJsaW5lYXItZ3JhZGllbnQiIHgxPSI3NC43NyIgeTE9IjY3LjMiIHgyPSIyNzcuMjMiIHkyPSI1MTIuNzIiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiMyOTRjYTciLz48c3RvcCBvZmZzZXQ9IjAuNDgiIHN0b3AtY29sb3I9IiM5NmE3ZDQiLz48c3RvcCBvZmZzZXQ9IjAuODQiIHN0b3AtY29sb3I9IiNlMWU2ZjMiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNmZmYiLz48L2xpbmVhckdyYWRpZW50PjxsaW5lYXJHcmFkaWVudCBpZD0ibGluZWFyLWdyYWRpZW50LTIiIHgxPSItMjI4Ljc0IiB5MT0iLTE0NC4yOSIgeDI9IjQ1MSIgeTI9IjY1MS44OSIgZ3JhZGllbnRUcmFuc2Zvcm09InRyYW5zbGF0ZSgwIDApIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjNjg3N2VjIi8+PHN0b3Agb2Zmc2V0PSIwLjI5IiBzdG9wLWNvbG9yPSIjOTdhMWYyIi8+PHN0b3Agb2Zmc2V0PSIwLjc3IiBzdG9wLWNvbG9yPSIjZTJlNGZiIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjZmZmIi8+PC9saW5lYXJHcmFkaWVudD48bGluZWFyR3JhZGllbnQgaWQ9ImxpbmVhci1ncmFkaWVudC0zIiB4MT0iLTE1MS4yMiIgeTE9Ii0yODUuOSIgeDI9IjQ1MC4wOCIgeTI9IjQzMC42MyIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzgzOTdjYyIvPjxzdG9wIG9mZnNldD0iMC4xNSIgc3RvcC1jb2xvcj0iIzk3YThkNCIvPjxzdG9wIG9mZnNldD0iMC43MyIgc3RvcC1jb2xvcj0iI2UyZTZmMyIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI2ZmZiIvPjwvbGluZWFyR3JhZGllbnQ+PHJhZGlhbEdyYWRpZW50IGlkPSJyYWRpYWwtZ3JhZGllbnQtMyIgY3g9IjI1OS42OCIgY3k9Ii0zNC43MSIgcj0iNDMxLjM3IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjZmZmIi8+PHN0b3Agb2Zmc2V0PSIxIi8+PC9yYWRpYWxHcmFkaWVudD48L2RlZnM+PHRpdGxlPmxvZ28tb3JpZ2FtaTwvdGl0bGU+PGcgY2xhc3M9ImNscy0xIj48ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIj48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0xNjguMDgsNTYwQTU3MC41NCw1NzAuNTQsMCwwLDAsNDU5Ljg0LDQwMy41OUw1Ni4yNSwwVjQ0OC4xN1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC01Ni4yNSkiLz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik01Ni4yNSw0NDguMTdDMzAzLjc3LDQ0OC4xNyw1MDQuNDIsMjQ3LjUyLDUwNC40MiwwSDU2LjI1WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTU2LjI1KSIvPjxwYXRoIGNsYXNzPSJjbHMtNCIgZD0iTTU2LjI1LDQ0OC4xN2gwTDczLjUsNDY1LjQyYzEyMS41Ny00LjQ1LDIzMS40LTU1LjY4LDMxMi0xMzYuMjNsLTEyLjI5LTEyLjI4QTQ0Ni44LDQ0Ni44LDAsMCwxLDU2LjI1LDQ0OC4xN1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC01Ni4yNSkiLz48cGF0aCBjbGFzcz0iY2xzLTUiIGQ9Ik0xNjguMDgsNTYwQTU3MC41NCw1NzAuNTQsMCwwLDAsNDU5Ljg0LDQwMy41OUw1Ni4yNSwwVjQ0OC4xN1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC01Ni4yNSkiLz48cGF0aCBjbGFzcz0iY2xzLTYiIGQ9Ik00NTkuODQsNDAzLjU5LDU2LjI1LDAsNDIzLjE0LDQzNy4xM0M0MzUuODMsNDI2LjQ2LDQ0OC4xMiw0MTUuMzEsNDU5Ljg0LDQwMy41OVoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC01Ni4yNSkiLz48cGF0aCBjbGFzcz0iY2xzLTciIGQ9Ik01Ni4yNSwwLDM3My4xNiwzMTYuOTFxNC4yMy00LjI1LDguMzUtOC42WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTU2LjI1KSIvPjwvZz48L2c+PC9zdmc+">
</a>

  <br>

<a href="https://github.com/pre-commit/pre-commit">
  <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white">
</a>
<a href="https://github.com/psf/black">
  <img alt="style: black" src="https://img.shields.io/badge/style-black-000000.svg">
</a>
<a href="https://wemake-python-stylegui.de/en/">
  <img alt="wemake-python-styleguide" src="https://img.shields.io/badge/style-wemake-000000.svg">
</a>

<br>

[![Continuous Integration](https://github.com/emma-heriot-watt/offline-inference/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/emma-heriot-watt/offline-inference/actions/workflows/continuous_integration.yml)
[![Tests](https://github.com/emma-heriot-watt/offline-inference/actions/workflows/tests.yml/badge.svg)](https://github.com/emma-heriot-watt/offline-inference/actions/workflows/tests.yml)

</div>

> [!IMPORTANT]
> If you have questions or find bugs or anything, you can contact us in our [organisation's discussion](https://github.com/orgs/emma-heriot-watt/discussions).

## About

We use code in this repository to generate new missions to facilitate self-play, to run the agent in the environment, and to evaluate the agent for the eval.ai leaderboard.

> [!IMPORTANT]
> We only ever ran this on a Ubuntu 20 Linux machine. This has not been tested or verified on MacOS or Windows. Your mileage may vary.

## Installing dependencies

You can run the convenience script at `scripts/prepare-user-area.sh`.

> [!CAUTION]
> I **HIGHLY RECOMMEND** reading the script to know what it does, because you might not need all of it!
> The convenience script does do some sudo-based file changes so if you don't want to permanently dirty your computer, look at it!

## Running things

> [!TIP]
> If you need sudo to run Docker, prefix the `poetry run` command with: `sudo -E env PATH=$PATH`.

### T1 evaluation (the one for [evai.ai](https://eval.ai/web/challenges/challenge-page/1903/overview))

When running T1, progress is sent to [wandb:emma-simbot/alexa-arena-evaluation](https://wandb.ai/emma-simbot/alexa-arena-evaluation). All session IDs are prefixed with `T1-`.

#### Steps

1. Create a new tmux session.
2. In one tmux pane, run `sudo /usr/bin/X :1 &`
3. In the other pane, run:

   ```bash
   poetry run python -m simbot_offline_inference run-background-services
   ```

4. Finally, in a third pane, run:

   ```bash
   poetry run python -m simbot_offline_inference run-their-evaluation
   ```

5. Let it run.

### Running the trajectory generation

When running trajectories, each one is a new "run", and all the runs are tracked at [wandb:emma-simbot/arena-high-level-trajectories](https://wandb.ai/emma-simbot/arena-high-level-trajectories).

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
