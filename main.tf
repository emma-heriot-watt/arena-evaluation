/* --------------------------------- Locals --------------------------------- */
locals {
  ami_prefix             = "EMMA-SimBot-Inference"
  ebs_volume_size        = 100
  instance_name          = "SimBot/OfflineInference"
  instance_type          = "g5.2xlarge"
  region                 = "us-east-1"
  role_name              = "Simbot-EC2-Role"
  ssh_key_name           = "amit-aws-us-east-1"
  stack_formation_prefix = "Simbot-University-Stack"
  user_data_path         = "scripts/instance-user-data.sh"
}

/* -------------------------------- Providers ------------------------------- */
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">=1.3.0"
}

provider "aws" {
  region = local.region

  default_tags {
    tags = {
      SimBot = "Evaluation"
    }
  }
}

/* ------------------------------ Data sources ------------------------------ */
data "aws_ami" "emma_simbot_inference" {
  most_recent = true
  filter {
    name   = "name"
    values = ["${local.ami_prefix}-*"]
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_security_group" "default" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "group-name"
    values = ["default"]
  }
}

data "aws_security_group" "ssh" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "group-name"
    values = ["SSH"]
  }
}

data "aws_iam_instance_profiles" "simbot_role_instance_profiles" {
  role_name = local.role_name
}

data "aws_iam_instance_profile" "simbot_instance_profile" {
  name = tolist(data.aws_iam_instance_profiles.simbot_role_instance_profiles.names)[0]
}

/* -------------------------------- Resources ------------------------------- */
resource "aws_security_group" "simbot_streaming_server" {
  name        = "SimBot/StreamingServer-SG"
  description = "Allow traffic needed for the streaming server"

  vpc_id = data.aws_vpc.default.id

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 81
    protocol    = "tcp"
    to_port     = 81
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 19302
    protocol    = "tcp"
    to_port     = 19302
  }
}

resource "aws_instance" "simbot_inference_ec2_instance" {
  ami           = data.aws_ami.emma_simbot_inference.id
  instance_type = local.instance_type

  vpc_security_group_ids = [
    aws_security_group.simbot_streaming_server.id,
    data.aws_security_group.default.id,
    data.aws_security_group.ssh.id,
  ]

  root_block_device {
    volume_size = local.ebs_volume_size
    volume_type = "gp3"
  }

  key_name             = local.ssh_key_name
  iam_instance_profile = data.aws_iam_instance_profile.simbot_instance_profile.name

  user_data = file(local.user_data_path)

  tags = {
    Name = local.instance_name
  }
}

/* --------------------------------- Outputs -------------------------------- */
