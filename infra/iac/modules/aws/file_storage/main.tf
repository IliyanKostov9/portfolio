terraform {
  required_providers {
    github = {
      source = "integrations/github"
    }
  }
}

locals {
  uppercase_name_without_dash = upper(strcontains(var.name, "-") ? replace(var.name, "-", "_") : var.name)
}

data "aws_caller_identity" "current" {}
resource "aws_s3_bucket" "current" {
  bucket = format("%s-%s-%s", var.name, var.env, data.aws_caller_identity.current.account_id)
  tags = {
    Environment = var.env
  }
}

resource "aws_s3_bucket_public_access_block" "disable_public_access" {
  bucket                  = format("%s-%s-%s", var.name, var.env, data.aws_caller_identity.current.account_id)
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "deny_http_access" {
  statement {
    sid    = "HTTPSOnly"
    effect = "Deny"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.current.arn,
      "${aws_s3_bucket.current.arn}/*"
    ]
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "deny_https_access" {
  bucket = format("%s-%s-%s", var.name, var.env, data.aws_caller_identity.current.account_id)
  policy = data.aws_iam_policy_document.deny_http_access.json
}

resource "aws_iam_user" "current" {
  name = format("portfolio-user-%s-%s", var.name, var.env)
  path = "/"

  tags = {
    Environment = var.env
  }
}


resource "aws_iam_access_key" "current" {
  user = aws_iam_user.current.name
}

resource "github_actions_secret" "aws_access_key_id" {
  repository      = "portfolio"
  secret_name     = format("PORTFOLIO_S3_%s_%s_ACCESS_KEY_ID", local.uppercase_name_without_dash, upper(var.env))
  plaintext_value = aws_iam_access_key.current.id
}

resource "github_actions_secret" "aws_secret_access_key" {
  repository      = "portfolio"
  secret_name     = format("PORTFOLIO_S3_%s_%s_SECRET_ACESS_KEY", local.uppercase_name_without_dash, upper(var.env))
  plaintext_value = aws_iam_access_key.current.secret
}

resource "github_actions_secret" "aws_bucket_name" {
  repository      = "portfolio"
  secret_name     = format("PORTFOLIO_S3_%s_%s_BUCKET", local.uppercase_name_without_dash, upper(var.env))
  plaintext_value = aws_s3_bucket.current.id
}


data "aws_iam_policy_document" "current" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:GetBucketLocation",
      "s3:ListBucket",
      "s3:DeleteObject",
      "s3:DeleteObjectVersion",
    ]
    resources = [
      aws_s3_bucket.current.arn,
      "${aws_s3_bucket.current.arn}/*"
    ]
  }
}

resource "aws_iam_user_policy" "current" {
  name   = format("portfolio-policy-%s-%s", var.name, var.env)
  user   = aws_iam_user.current.name
  policy = data.aws_iam_policy_document.current.json
}
