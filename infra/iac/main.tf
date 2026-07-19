module "s3_main_storage" {
  source = "./modules/aws/file_storage"
  env    = var.env
  name   = "main"
}

import {
  to = module.s3_main_storage.aws_s3_bucket.current
  id = format("%s-%s-%s", "main", var.env, var.account_id)
}

import {
  to = module.s3_main_storage.aws_iam_user.current
  id = format("portfolio-user-%s-%s", "main", var.env)
}


module "s3_polly" {
  source = "./modules/aws/file_storage"
  env    = var.env
  name   = "polly"
  iam_user_policy_additional_statements = [
    {
      sid       = "AllowPollyActions"
      effect    = "Allow"
      actions   = ["polly:SynthesizeSpeech", "polly:DescribeVoices"]
      resources = ["*"]
    }
  ]
}

module "ses_email_identity_one" {
  source             = "./modules/aws/send_email"
  env                = var.env
  domain             = var.email_domain
  zone_id            = var.zone_id
  ses_identity_email = var.ses_identity_email
}

import {
  to = module.ses_email_identity_one.aws_iam_user.current
  id = format("ses-user-%s", var.env)
}

<<<<<<< HEAD
module "assets_storage" {
  source                                = "./modules/aws/host_web_assets"
  env                                   = var.env
  region                                = var.region
  cfn_domain                            = var.cfn_assets_domain
  domain                                = var.domain
  cloudfront_origin_access_control_name = format("portfolio-assets-%s", var.env)
  bucket_assets_name                    = "portfolio-assets"
  s3_origin_id                          = "portfolio-assets-origin"

  providers = {
    aws           = aws
    aws.us_east_1 = aws.us_east_1
  }
}

=======
>>>>>>> a7a3609 (Chore/arrange configuration (#393))
