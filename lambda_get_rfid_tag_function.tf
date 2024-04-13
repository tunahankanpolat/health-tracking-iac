module "get_rfid_tag_function" {
  source = "./lambda"
  execution_role_arn = aws_iam_role.all_lambda_role.arn
  src_directory_name = "get_rfid_tag_function"
}

resource "aws_lambda_function_url" "get_rfid_tag_function" {
  function_name      = module.get_rfid_tag_function.function_name
  authorization_type = "NONE"
}