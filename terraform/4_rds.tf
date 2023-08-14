module "rds_instance" {
    source = "cloudposse/rds/aws"
    # Cloud Posse recommends pinning every module to a specific version
    version = "0.41.0"

    vpc_id                      = module.vpc.vpc_id
    subnet_ids                  = module.subnets.private_subnet_ids
    security_group_ids          = [module.vpc.vpc_default_security_group_id]
    allowed_cidr_blocks         = [var.vpc_cidr]

    context = module.this.context
    publicly_accessible         = var.publicly_accessible
    apply_immediately           = var.apply_immediately

    //host_name                   = "db"
    database_name               = var.DATABASE_NAME
    database_user               = var.DATABASE_USER
    database_password           = var.DATABASE_PASSWORD
    database_port               = var.DATABASE_PORT
    multi_az                    = var.multi_az

    storage_type                = "gp2"
    allocated_storage           = 100

    engine                      = var.engine
    engine_version              = var.engine_version
    instance_class              = var.instance_class
    db_parameter_group          = var.db_parameter_group
    
    skip_final_snapshot         = false
    copy_tags_to_snapshot       = true
    backup_retention_period     = 7

}