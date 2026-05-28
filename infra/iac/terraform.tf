terraform {
  required_version = ">= 1.2.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.41"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.2"
    }

    external = {
      source  = "hashicorp/external"
      version = "~> 2.3"
    }
  }

  backend "s3" {
    bucket = "tf-state-405466951648"
    key    = "states/prod/terraform.tfstate"
    region = "eu-west-1"

    dynamodb_table = "terraform-state-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.region
}

provider "github" {
  owner = "IliyanKostov9"
  token = var.github_token
}
