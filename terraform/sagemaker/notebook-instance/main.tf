provider "aws" {
    region = "us-east-1"
}

resource "aws_sagemaker_notebook_instance" "sagemaker_notebook_instance" {
    name = "my-notebook-instance"
    instance_type = "ml.t2.medium"
    role_arn = aws_iam_role.sagemaker_execution_role.arn
}