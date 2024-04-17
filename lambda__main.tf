resource "aws_iam_role" "all_lambda_role" {
  name = "all_lambda_role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "AWSLambda_FullAccess" {
  policy_arn = "arn:aws:iam::aws:policy/AWSLambda_FullAccess"
  role       = aws_iam_role.all_lambda_role.name
}
resource "aws_iam_role_policy_attachment" "AmazonDynamoDBFullAccess" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  role       = aws_iam_role.all_lambda_role.name
}
resource "aws_iam_role_policy_attachment" "AWSLambdaBasicExecutionRole" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.all_lambda_role.name
}
resource "aws_iam_role_policy_attachment" "AmazonS3FullAccess" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  role       = aws_iam_role.all_lambda_role.name
}

resource "aws_lambda_layer_version" "dependencies_layer" {
  filename            = "${local.lambda_layers_path}/dependencies/python.zip"
  layer_name          = "dependencies"
  description         = "Custom dependency layer"
  compatible_runtimes = [
    "python3.12",
  ]
  source_code_hash = filebase64sha256("${local.lambda_layers_path}/dependencies/python.zip")
}
