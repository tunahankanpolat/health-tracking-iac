resource "aws_dynamodb_table" "drug_box" {
  name = "drug_box"
  hash_key = "mac_address"
    
  attribute {
    name = "mac_address"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "N"
  }

  read_capacity  = 1
  write_capacity = 1

  global_secondary_index {
    hash_key           = "user_id"
    name               = "user_id_index"
    projection_type    = "ALL"
    read_capacity      = 1
    write_capacity     = 1
  }
}

resource "aws_dynamodb_table" "lock_log" {
  name = "lock_log"
  hash_key = "mac_address"
  
  attribute {
    name = "mac_address"
    type = "S"
  }
  read_capacity  = 1
  write_capacity = 1
}

resource "aws_dynamodb_table" "user" {
  name = "user"
  hash_key = "user_id"
  
  attribute {
    name = "user_id"
    type = "N"
  }
  read_capacity  = 1
  write_capacity = 1
}


resource "aws_dynamodb_table" "user_health_data" {
  name           = "user_health_data"
  hash_key       = "entry_id"

  attribute {
    name = "entry_id"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "N"
  }

  attribute {
    name = "time_stamp"
    type = "N"
  }

  read_capacity  = 1
  write_capacity = 1

  global_secondary_index {
    hash_key           = "user_id"
    range_key          = "time_stamp"  # Added as sort key
    name               = "user_id_timestamp_index"
    projection_type    = "ALL"
    read_capacity      = 1
    write_capacity     = 1
  }
}
