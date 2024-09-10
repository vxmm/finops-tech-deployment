output "s3_bucket_input_arn" {
  value = aws_s3_bucket.project_stocks_vxmm.arn
}

output "s3_bucket_output_arn" {
  value = aws_s3_bucket.output_stocks_vxmm.arn
}

output "project_stocks_vxmm_bucket" {
  value = aws_s3_bucket.project_stocks_vxmm.bucket
}