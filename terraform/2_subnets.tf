#############################################################
# Subnets Defenitions
#############################################################

  module "subnets" {
    source = "cloudposse/dynamic-subnets/aws"
    # Cloud Posse recommends pinning every module to a specific version
    version = "2.0.4"
    
    availability_zones   = var.availability_zones
    vpc_id               = module.vpc.vpc_id
    igw_id               = [module.vpc.igw_id]
    ipv4_cidr_block      = [module.vpc.vpc_cidr_block]
    nat_gateway_enabled  = true
    nat_instance_enabled = false
  
    context = module.this.context
  }
