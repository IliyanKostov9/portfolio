output "arn" {
  description = "ARN of S3"
  value       = aws_s3_bucket.current.arn
}

output "regional_domain_name" {
  description = "S3 regional domain name"
  value       = aws_s3_bucket.current.bucket_regional_domain_name
}
