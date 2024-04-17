resource "aws_cloudwatch_event_rule" "schedule" {
  count = var.schedule_expression != "" ? 1 : 0

  name                = aws_lambda_function.this.function_name
  description         = "${aws_lambda_function.this.function_name} Schedule"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "this" {
  count = var.schedule_expression != "" ? 1 : 0

  target_id = aws_lambda_function.this.function_name
  rule      = aws_cloudwatch_event_rule.schedule[count.index].name
  arn       = aws_lambda_function.this.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_control" {
  count = var.schedule_expression != "" ? 1 : 0

  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule[count.index].arn
}