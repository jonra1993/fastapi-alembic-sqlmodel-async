terraform {
  cloud {
    organization = "jrtec"

    workspaces {
      name = "jrtec-fastapi-alembic-sqlmodel-async-workspace"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.57.0"
    }
    local = {
      version = ">= 2.2.3"
    }
    tls = {
      source  = "hashicorp/tls"
      version = ">= 3.0"
    }
  }
  required_version = ">= 1.2.3"
}