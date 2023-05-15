# Offline Inference on the SimBot arena

## Creating the instance

Use the terraform configuation included to build/destroy the instance.

#### Terraform commands you need to know to do things

- `terraform init` — Initialise your terraform environment
- `terraform plan` — Verify things can be deployed correctly on AWS, and catch _most_ confirmation errors
- `terraform apply` — Create the instances and connect all the resources.[^1]
- `terraform destroy` — Terminate the instance and remove any resources that were newly-created.[^2]

[^1]: _You can use the [EC2 serial console](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-serial-console.html) to watch the instance start up and watch the outputs of the `user-data` script. There is no history so if the serial console is blank, you have missed whatever it said before._
[^2]: _Only resources that were created will be removed, and nothing that existed beforehand. Therefore, you can call this whenever you want and trust that nothing else will be destroyed._

## Running the evaluation

The session IDs are all prefixed with `T2-`, ~~and therefore can be found in OpenSearch with all the other session turns~~.

> **Warning**
> There are a lot of settings in `src/simbot_offline_inference/settings.py` which control and change the behaviour when running things. I recommend knowing what exists there.

1. Create the tmux session with `tmux -CC new -A -s main`
2. Create 3 tmux panes
3. In one pane, run `sudo /usr/bin/X :1 &`
4. In the other pane, first run:

   ```bash
   cd offline-inference \
   && poetry env use $(pyenv which python) \
   && poetry install \
   && poetry shell
   ```

   and then run:

   ```bash
   sudo -E env PATH=$PATH poetry run python -m simbot_offline_inference run-background-services
   ```

5. Finally, in a third pane, run:

   ```bash
   sudo -E env PATH=$PATH LOG_LEVEL=DEBUG poetry run python -m simbot_offline_inference run-their-evaluation T1
   ```

6. Let it run.

## Running the trajectory generation

> **Warning**
> There are a lot of settings in `src/simbot_offline_inference/settings.py` which control and change the behaviour when running things. I recommend knowing what exists there.

1. Create the tmux session with `tmux -CC new -A -s main`
2. Create 3 tmux panes
3. In one pane, run `sudo /usr/bin/X :1 &`
4. In the other pane, first run:

   ```bash
   cd offline-inference \
   && poetry env use $(pyenv which python) \
   && poetry install \
   && poetry shell
   ```

   and then run:

   ```bash
   sudo -E env PATH=$PATH poetry run python -m simbot_offline_inference run-background-services
   ```

5. Finally, in a third pane, run:

   ```bash
   sudo -E env PATH=$PATH LOG_LEVEL=DEBUG poetry run python -m simbot_offline_inference run-their-evaluation T1
   ```

6. Let it run.
