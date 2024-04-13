resource "aws_dynamodb_table" "rfid_tag" {
  name = "rfid_tag"
  hash_key = "mac_address"
    
  attribute {
    name = "mac_address"
    type = "S"
  }
  read_capacity  = 10
  write_capacity = 10
}

resource "aws_dynamodb_table" "lock_log" {
  name = "lock_log"
  hash_key = "mac_address"
  
  attribute {
    name = "mac_address"
    type = "S"
  }
  read_capacity  = 10
  write_capacity = 10
}
