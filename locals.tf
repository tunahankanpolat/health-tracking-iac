locals {
  lambda_layers_path = "${path.module}/lambda/layers"

  hourly_schedule                         = "cron(0 * * * ? *)"
  daily_schedule_11pm                     = "cron(0 19 * * ? *)"
  daily_schedule_at_quarter_past_11pm     = "cron(15 19 * * ? *)"
  daily_schedule_midnight                 = "cron(0 00 * * ? *)"
  daily_schedule_at_quarter_past_midnight = "cron(15 00 * * ? *)"
  weekly_schedule                         = "cron(0 9 ? * MON *)"
  monthly_schedule_first_day_at_3_am      = "cron(0 3 1 * ? *)"

  mime_types = jsondecode(file("${path.module}/mime.json"))
}