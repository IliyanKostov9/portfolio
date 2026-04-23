resource "aws_iam_user" "current" {
  name = format("ses-user-%s", var.env)
  path = "/"

  tags = {
    Environment = var.env
  }
}


resource "aws_iam_access_key" "current" {
  user = aws_iam_user.current.name
}

resource "aws_iam_user_policy" "current" {
  name = format("ses-policy-%s", var.env)
  user = aws_iam_user.current.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ses:SendRawEmail"]
        Resource = ["*"]
      }
    ]
  })
}

resource "aws_ses_domain_identity" "current" {
  domain = var.domain
}

resource "aws_route53_record" "current" {
  zone_id = var.zone_id
  name    = format("_amazonses.%s", var.domain)
  type    = "TXT"
  ttl     = "600"
  records = [aws_ses_domain_identity.current.verification_token]
}

resource "aws_ses_email_identity" "identity" {
  email = var.ses_identity_email
}
