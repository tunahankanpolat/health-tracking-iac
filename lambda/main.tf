locals {
  src_path      = "${path.module}/../src"
  build_path    = "${path.module}/../build"
  resource_path = "${path.module}/../resources"
}

data "archive_file" "this" {
  type             = "zip"
  output_file_mode = "0644"
  source_dir       = "${local.src_path}/${var.src_directory_name}/"
  output_path      = "${local.build_path}/${var.src_directory_name}.zip"
}

locals {
  function_name  = replace(title(replace(var.src_directory_name, "_", " ")), " ", "_")
  log_group_name = "/aws/lambda/${local.function_name}"
}   

resource "aws_lambda_function" "this" {
  function_name                  = local.function_name
  filename                       = data.archive_file.this.output_path
  source_code_hash               = data.archive_file.this.output_base64sha256
  role                           = var.execution_role_arn
  layers                         = var.layer_arns
  runtime                        = "python3.12"
  handler                        = "lambda_function.lambda_handler"
  reserved_concurrent_executions = var.lambda_reserved_concurrency
  timeout                        = 900
  memory_size                    = 128
}

resource "aws_cloudwatch_log_group" "this" {
  name = local.log_group_name
}