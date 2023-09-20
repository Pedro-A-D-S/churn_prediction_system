provider "aws" {
    region = var.region
}

resource "aws_sagemaker_domain" "mlops-sagemaker-pipeline" {
  domain_name = "mlops-sagemaker-pipeline"
  auth_mode = "IAM"
  vpc_id = var.vpc_id
  subnet_ids = var.subnet_ids

  default_user_settings {
    execution_role = var.role_arn
  }
}