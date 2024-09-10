resource "aws_lambda_function" "lseg_lambda" {
  filename      = var.lambda_zip_file
  function_name = "lseg-lambda"
  role          = var.iam_role_arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  timeout       = 20
}