resource "aws_dynamodb_table" "lpa_codes" {
  name             = "lpa-codes-${local.environment}"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "code"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "code"
    type = "S"
  }

  attribute {
    name = "lpa"
    type = "S"
  }

  attribute {
    name = "actor"
    type = "S"
  }

  ttl {
    attribute_name = "expiry_date"
    enabled        = true
  }

  global_secondary_index {
    name            = "key_index"
    hash_key        = "actor"
    range_key       = "lpa"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = local.account.pit_recovery_flag
  }

  tags = local.default_tags
}

//dynamodb for dev env only for branch deletion

resource "aws_dynamodb_table" "workspace_cleanup_table" {
  count        = local.account.account_mapping == "development" ? 1 : 0
  name         = "WorkspaceCleanup"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "WorkspaceName"

  attribute {
    name = "WorkspaceName"
    type = "S"
  }

  ttl {
    attribute_name = "ExpiresTTL"
    enabled        = true
  }

  lifecycle {
    prevent_destroy = false
  }
}
