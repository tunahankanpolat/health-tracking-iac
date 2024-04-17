module "scheduled_fetch_fit_data_function" {
  source = "./lambda"
  execution_role_arn = aws_iam_role.all_lambda_role.arn
  src_directory_name = "scheduled_fetch_fit_data_function"
  layer_arns         = [
    aws_lambda_layer_version.dependencies_layer.arn,
  ]
  schedule_expression = local.daily_schedule_midnight
}

resource "aws_lambda_function_url" "scheduled_fetch_fit_data_function" {
  function_name      = module.scheduled_fetch_fit_data_function.function_name
  authorization_type = "NONE"
}
