resource "aws_s3_bucket" "project_stocks_vxmm" {
  bucket = format("%s-%s", var.input_bucket, var.region)
}

resource "aws_s3_bucket" "output_stocks_vxmm" {
  bucket = format("%s-%s", var.output_bucket, var.region)
}