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
    principals = optional(object({
      type        = string
      identifiers = list(string)
    }))
    condition = optional(object({
      test     = string
      variable = string
      values   = list(string)
    }))
  }))
  default = []
}

variable "iam_bucket_policy_additional_statements" {
  description = "Additional permissions for bucket iam policies"
  type = list(object({
    sid       = string
    effect    = string
    actions   = list(string)
    resources = list(string)
    principals = optional(object({
      type        = string
      identifiers = list(string)
    }))
    condition = optional(object({
      test     = string
      variable = string
      values   = list(string)
    }))
  }))
  default = []
}
