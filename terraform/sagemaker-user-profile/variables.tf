variable "name" {
    type = string
    description = "The name of the SageMaker user profile"
    default = "mlops-sagemaker"
}

variable "execution_role_arn" {
    type = string
    description = "The ARN of the IAM role that the SageMaker user profile will use to execute SageMaker jobs."
    default = "sagemaker-role"
}

variable "user_settings_tags" {
    type = map(string)
    description = "A map of tags for the SageMaker user profile"
    default = {
        mlops = "sagemaker"
    }
}

variable "jupyter_server_instance_type" {
    type = string
    description = "The instance type for the JupyterServer app in the SageMaker user profile."
    default = "ml.t2.micro"
}

variable "enable_canvas_base_permissions" {
    type = bool
    description = "Whether to enable Canvas base permissions for the SageMaker user profile."
    default = true
}

variable "system_managed_canvas_storage_configuration" {
    type = bool
    description = "Whether to use the system managed Canvas storage configuration."
    default = true
}

variable "enable_canvas_ready_to_use_models" {
    type = bool
    description = "Whether to enable Canvas ready-to-use models for the SageMaker user profile."
    default = true
}

variable "enable_time_series_forecasting" {
    type = bool
    description = "Whether to enable time series forecasting for the SageMaker user profile."
    default = true
}

variable "create_and_use_new_execution_role" {
    type = bool
    description = "Whether to create and use a new execution role for the SageMaker user profile."
    default = true
}

variable "enable_model_registry_registration_permissions" {
    type = bool
    description = "Whether to enable model registry registration permissions for the SageMaker user profile."
    default = true
}