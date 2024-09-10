output "lambda_arn" {
  value = aws_lambda_function.lseg_lambda.arn
}

output "lambda_name" {
  value = aws_lambda_function.lseg_lambda.function_name
}