variable "region" {
    description = "Region where to deploy resources to"
}

variable "access_key" {
    description = "Access key for AWS service account"
}

variable "secret_key" {
  description = "Secret key for AWS service account"
}

data "aws_ami" "image" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

provider "aws" {
    region = var.region
    access_key = var.access_key
    secret_key = var.secret_key
}