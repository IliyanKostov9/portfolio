module "s3_main_storage" {
  source = "./modules/aws/file_storage"
  env    = var.env
  name   = "main"
}

module "s3_polly" {
  source = "./modules/aws/file_storage"
  env    = var.env
  name   = "text-to-speech"
}

module "ses_email_identity_one" {
  source             = "./modules/aws/send_email"
  env                = var.env
  domain             = var.domain
  zone_id            = var.zone_id
  ses_identity_email = var.ses_identity_email
}
