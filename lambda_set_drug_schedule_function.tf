module "set_drug_schedule_function" {
  source = "./lambda"
  execution_role_arn = aws_iam_role.all_lambda_role.arn
  src_directory_name = "set_drug_schedule_function"
  layer_arns         = [
    aws_lambda_layer_version.dependencies_layer.arn,
  ]
}

resource "aws_lambda_function_url" "set_drug_schedule_function" {
  function_name      = module.set_drug_schedule_function.function_name
  authorization_type = "NONE"
  
  cors {
    allow_headers = ["content-type", "access_control_allow_origin"]
    allow_origins = ["*"]
    allow_methods = ["POST"]
  }
}