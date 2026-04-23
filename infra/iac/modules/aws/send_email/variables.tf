variable "env" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
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
  description = "User email for the identity"
  type        = string
}


