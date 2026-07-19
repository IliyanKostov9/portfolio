module "s3_assets" {
  source = "./modules/aws/file_storage"
  env    = var.env
  name   = format("%s-assets", var.name)
  iam_user_policy_additional_statements = [
    {
      sid       = "AllowPollyActions"
      effect    = "Allow"
      actions   = ["polly:SynthesizeSpeech", "polly:DescribeVoices"]
      resources = ["*"]
    }
  ]
}

