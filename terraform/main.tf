module "sagemaker-execution-role" {
    source = "./sagemaker/sagemaker-execution-role"
    role_name = "sagemaker-role"
    region = "us-east-1"
}

module "sagemaker-domain" {
    source = "./sagemaker/sagemaker-domain"
    region = "us-east-1"
    role_arn = module.sagemaker-execution-role.role_arn
}

module "sagemaker-user-profile" {
    source = "./sagemaker/sagemaker-user-profile"

    name = "mlops-sagemaker"
}