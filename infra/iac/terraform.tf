terraform {
  required_version = ">= 1.2.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.41"
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
