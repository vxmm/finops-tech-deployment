resource "aws_iam_role" "lseg_lambda_role" {
  name = "lseg-lambda-role"
  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda-attach-custom-policy" {
  role       = aws_iam_role.lseg_lambda_role.name
  policy_arn = aws_iam_policy.lseg_lambda_policy.arn
}


resource "aws_iam_role_policy_attachment" "lambda-attach-managed-policy" {
  role       = aws_iam_role.lseg_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}