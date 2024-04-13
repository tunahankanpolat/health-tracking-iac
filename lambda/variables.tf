variable "src_directory_name" {
  type        = string
  description = "Lambda source directory name"
}

variable "execution_role_arn" {
  type        = string
  description = "ARN for Lambda Execution Role"
}

variable "lambda_reserved_concurrency" {
  type        = number
  description = "The amount of reserved concurrent executions for this lambda function"
  default     = -1
}