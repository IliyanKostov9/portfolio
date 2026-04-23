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

  cloud {
    organization = "iliyan-personal"
    workspaces {
      name = "portfolio"
    }
  }
}

provider "aws" {
  region = var.region
}

provider "github" {
  token = var.github_token
}
