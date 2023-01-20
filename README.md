# Offline Inference on the SimBot arena

## Creating the instance

Use the terraform configuation included to build/destroy the instance.

### Initialise terraform environment

```bash
terraform init
```

### Verify the terraform configuration _should_ work

This will verify that things can be deployed correctly on AWS and will catch _most_ configuration errors.

```bash
terraform plan
```

### Create the instance

This will create the instance and any associated resources necessary. You can use the [EC2 serial console](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-serial-console.html) to watch the instance start up and watch the outputs of the `user-data` script[^1].

```bash
terraform apply
```

[^1]: _There is no history so if the serial console is blank, you have missed whatever it said before._

### Clean up resources

When you are finished, **clean up your mess!** This command will only destroy the instance and any newly-created resources for the project, and not destroy anything else, and so you can do this knowing that nothing important will be destroyed.

```bash
terraform destroy
```

## Running the evaluation

1. SSH into the instance
1. Create the tmux session with `tmux -CC new -A -s main`
