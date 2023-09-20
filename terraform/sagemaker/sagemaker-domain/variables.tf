variable "role_name" {
    type = string
    description = "The AWS region to create the SageMaker domain."
    default = "sagemaker-role"
}

variable "region" {
    type = string
    description = "The ID of the VPC where to create the SageMaker domain"
    default = "us-east-1"
}

variable "vpc_id" {
    type = string
    description = "THe ID of the VPC where to create the SageMaker domain"
    default = "vpc-0d20bb0df23f74cc2"
}

variable "subnet_ids" {
    type = list(string)
    description = "A list of subnet IDs in the VPC where to create the SageMaker domain"
    default = ["subnet-0b94b47ea6ca1e241", "subnet-0d9aefb3e32b4714d"]
}

variable "role_arn" {
    type = string
    description = "The ARN of the SageMaker execution role."
}

variable "instance_type" {
    type = string
    description = "the instance type used for sagemaker domain."
    default = "ml.t2.micro"
}