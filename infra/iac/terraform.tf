terraform {
  required_version = ">= 1.2.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.41"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.11"
    }
  }

  backend "s3" {
    bucket = "tf-state-portfolio1-405466951648"
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
