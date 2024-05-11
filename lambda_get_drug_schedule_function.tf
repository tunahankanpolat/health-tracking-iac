module "get_drug_schedule_function" {
  source = "./lambda"
  execution_role_arn = aws_iam_role.all_lambda_role.arn
  src_directory_name = "get_drug_schedule_function"
  layer_arns         = [
    aws_lambda_layer_version.dependencies_layer.arn,
  ]
}

resource "aws_lambda_function_url" "get_drug_schedule_function" {
  function_name      = module.get_drug_schedule_function.function_name
  authorization_type = "NONE"
}