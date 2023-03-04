module "elastic_beanstalk_application" {
  source  = "cloudposse/elastic-beanstalk-application/aws"
  version = "0.11.1"

  description = "Test Elastic Beanstalk application"

  context = module.this.context
}

module "elastic_beanstalk_environment" {
  source = "cloudposse/elastic-beanstalk-environment/aws"
  version = "0.47.2"

  
  elastic_beanstalk_application_name = module.elastic_beanstalk_application.elastic_beanstalk_application_name
  environment_type                   = "LoadBalanced"
  loadbalancer_type                  = "application"
  region                             = var.aws_region
  autoscale_min                      = 1
  force_destroy                      = var.force_destroy

  instance_type    = var.instance_type
#   root_volume_size = var.root_volume_size
#   root_volume_type = var.root_volume_type

  vpc_id               = module.vpc.vpc_id
  loadbalancer_subnets = module.subnets.public_subnet_ids
  application_subnets  = module.subnets.private_subnet_ids

  allow_all_egress = true

  additional_security_group_rules = [
    {
      type                     = "ingress"
      from_port                = 0
      to_port                  = 65535
      protocol                 = "-1"
      source_security_group_id = module.vpc.vpc_default_security_group_id
      description              = "Allow all inbound traffic from trusted Security Groups"
    }
  ]

  # https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html
  # https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html#platforms-supported.docker
  solution_stack_name = "64bit Amazon Linux 2 v3.5.3 running Docker"

  env_vars = {
    for obj in concat(local.fastapi, local.database, local.traefik, local.redis, local.minio, local.external_apis) : "${obj.name}" => "${obj.value}"
  }

  extended_ec2_policy_document = data.aws_iam_policy_document.minimal_s3_permissions.json
  prefer_legacy_ssm_policy     = false
  prefer_legacy_service_policy = false

  context = module.this.context
}

data "aws_iam_policy_document" "minimal_s3_permissions" {
  statement {
    sid = "AllowS3OperationsOnElasticBeanstalkBuckets"
    actions = [
      "s3:ListAllMyBuckets",
      "s3:GetBucketLocation"
    ]
    resources = ["*"]
  }
}