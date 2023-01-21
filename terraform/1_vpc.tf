#############################################################
# Virtual private cloud Defenitions
#############################################################

module "vpc" {
  source = "cloudposse/vpc/aws"
  # Cloud Posse recommends pinning every module to a specific version
  version = "2.0.0"
  
  ipv4_primary_cidr_block = var.vpc_cidr

  context = module.this.context
}