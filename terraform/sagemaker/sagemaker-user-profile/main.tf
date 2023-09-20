module "sagemaker-domain" {
    source = "../sagemaker-domain"
}

resource "aws_sagemaker_user_profile" "mlops-sagemaker" {
    name = var.name
    domain_id = module.sagemaker-domain.domain_id
    user_settings {
        tags = var.user_settings_tags
        jupyter_server_app_settings {
            default_resource_spec {
                instance_type = var.jupyter_server_instance_type
            }
        }
    canvas_settings {
        enable_canvas_base_permissions = var.enable_canvas_base_permissions
        system_managed_canvas_storage_configuration = var.system_managed_canvas_storage_configuration
        enable_canvas_ready_to_use_models = var.enable_canvas_ready_to_use_models
        enable_time_series_forecasting = var.enable_time_series_forecasting
        create_and_use_new_execution_role = var.create_and_use_new_execution_role
        enable_model_registry_registration_permissions = var.enable_model_registry_registration_permissions
    }
    }
}