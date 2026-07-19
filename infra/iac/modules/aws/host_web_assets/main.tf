module "s3_assets" {
  source = "../file_storage"
  env    = var.env
  name   = format("%s-assets", var.bucket_assets_name)
  iam_user_policy_additional_statements = [
    {
      sid       = "AllowCloudFrontServicePrincipalWrite"
      effect    = "Allow"
      actions   = ["s3:GetObject", "s3:PutObject"]
      resources = ["${module.s3_assets.arn}/*"]
      principals = {
        type        = "Service"
        identifiers = ["cloudfront.amazonaws.com"]
      }
      condition = {
        test     = "StringEquals"
        variable = "AWS:SourceArn"
        values   = [aws_cloudfront_distribution.distro.arn]
      }
    }
  ]
}

data "aws_route53_zone" "main" {
  name = var.domain
}

resource "aws_acm_certificate" "domain" {
  provider          = aws.us_east_1
  domain_name       = var.cfn_domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.domain.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  zone_id         = data.aws_route53_zone.main.zone_id
  name            = each.value.name
  type            = each.value.type
  records         = [each.value.record]
  ttl             = 60
  allow_overwrite = true
}

resource "aws_acm_certificate_validation" "domain" {
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.domain.arn
  validation_record_fqdns = [for r in aws_route53_record.cert_validation : r.fqdn]
}



resource "aws_cloudfront_origin_access_control" "default" {
  name                              = var.cloudfront_origin_access_control_name
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "distro" {
  origin {
    domain_name              = module.s3_assets.regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.default.id
    origin_id                = var.s3_origin_id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distro"
  default_root_object = "index.html"

  aliases = [var.cfn_domain]

  default_cache_behavior {
    allowed_methods  = ["GET"]
    cached_methods   = ["GET"]
    target_origin_id = var.s3_origin_id

    forwarded_values {
      query_string = false
      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }
  price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["US", "CA", "GB", "DE"]
    }
  }

  tags = {
    Environment = var.env
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.domain.arn
    ssl_support_method  = "sni-only"
  }
}

resource "aws_route53_record" "cloudfront" {
  for_each = aws_cloudfront_distribution.distro.aliases
  zone_id  = data.aws_route53_zone.main.zone_id
  name     = each.value
  type     = "A"

  alias {
    name                   = aws_cloudfront_distribution.distro.domain_name
    zone_id                = aws_cloudfront_distribution.distro.hosted_zone_id
    evaluate_target_health = false
  }
}
