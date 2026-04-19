variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "env" {
  description = "Environment of the application"
  type        = string
  default     = "prod"
}

variable "domain" {
  description = "The Route53 domain name"
  type        = string
}

variable "zone_id" {
  description = "Zone id from Route53"
  type        = string
}


variable "ses_identity_email" {
  description = "Identity email for the SES"
  type        = string
}
