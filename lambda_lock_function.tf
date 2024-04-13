module "lock_function" {
  source = "./lambda"
  execution_role_arn = aws_iam_role.all_lambda_role.arn
  src_directory_name = "lock_function"
}

resource "aws_lambda_function_url" "lock_function" {
  function_name      = module.lock_function.function_name
  authorization_type = "NONE"
}
