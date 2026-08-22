variable "bucket_assets_name" {
  description = "The S3 buckets name"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "env" {
  description = "Environment"
  type        = string
  default     = "prod"
}

variable "cfn_domain" {
  description = "domain of the CloudFront"
  type        = string
}

variable "domain" {
  description = "domain of the CloudFront"
  type        = string
}

variable "cloudfront_origin_access_control_name" {
  description = "The name of Cloudfront access control name"
  type        = string
}

variable "s3_origin_id" {
  description = "S3 origin id"
  type        = string
}

