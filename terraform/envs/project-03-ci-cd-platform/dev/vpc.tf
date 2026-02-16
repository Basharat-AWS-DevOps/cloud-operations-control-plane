module "vpc" {
  source = "../../../modules/vpc"

  name                   = "${var.project_name}-${var.environment}"
  cidr_block             = var.vpc_cidr
  az_count               = 2
  enable_private_subnets = true

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
