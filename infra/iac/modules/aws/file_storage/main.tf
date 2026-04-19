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

resource "aws_s3_bucket_policy" "deny_https_access" {
  bucket = format("%s-%s-%s", var.name, var.env, data.aws_caller_identity.current.account_id)
  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "Block HTTP access"
    Statements = [
      {
        Sid    = "HTTPSOnly"
        Effect = "Deny"
        Principal = {
          "AWS" : "*"
        }
        Action = ["s3:*"]
        Resource = [
          aws_s3_bucket.current.arn,
          "${aws_s3_bucket.current.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" : "false"
          }
        }
      }
    ]
  })
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
data "aws_iam_policy_document" "current" {
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.current.arn,
      "${aws_s3_bucket.current.arn}/*"
    ]
  }
}

resource "aws_iam_user_policy" "current" {
  name   = format("ses-policy-%s", var.env)
  user   = aws_iam_user.current.name
  policy = data.aws_iam_policy_document.current.json
}
