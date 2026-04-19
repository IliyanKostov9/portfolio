resource "aws_s3_bucket" "main_bucket" {
  bucket           = format("%s-%s", var.name, var.env)
  bucket_namespace = "account-regional"

  tags = {
    Environment = var.env
  }

}
