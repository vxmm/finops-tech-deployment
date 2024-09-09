terraform {
    backend "s3" {
    }
}

module "iam" {
  source = "./iam"
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "lseg_lambda" {

  filename = "lambda_function_payload.zip"
  function_name = "lseg-lambda"
  role = module.iam.iam_role_arn
  handler = "lambda_function.lambda_handler"  
  runtime = "python3.12"
  timeout = 20
}  

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = format("%s-%s", var.input_bucket, var.region)

  lambda_function {
    lambda_function_arn = aws_lambda_function.lseg_lambda.arn
    events              = ["s3:ObjectCreated:Put"]
  }
  depends_on = [aws_lambda_permission.allow_s3_invocation]
}

resource "aws_s3_bucket" "project_stocks_vxmm" {
bucket = format("%s-%s", var.input_bucket, var.region)
}

resource "aws_s3_bucket" "output-stocks-vxmm" {
bucket = format("%s-%s", var.output_bucket, var.region)
  }

resource "aws_lambda_permission" "allow_s3_invocation" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lseg_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.project_stocks_vxmm.arn
}