module "s3_main_storage" {
  source = "../../modules/aws/s3"
  env    = var.env
  name   = "main"
}

module "s3_polly" {
  source = "../../modules/aws/s3"
  env    = var.env
  name   = "text-to-speech"
}
