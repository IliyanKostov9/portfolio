variable "env" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "name" {
  description = "The name of the bucket"
  type        = string
}

variable "iam_user_policy_additional_statements" {
  description = "Additional permissions for user iam policies"
  type = list(object({
    sid       = string
    effect    = string
    actions   = list(string)
    resources = list(string)
  }))
  default = []
}
