data "template_file" "lseg_lambda_policy" {
  template = file("./iam/lseg-lambda-policy.json.tpl")
  vars = {
    region = var.region
  }
}

resource "aws_iam_policy" "lseg_lambda_policy" {
  name   = "lseg-lambda-policy"
  policy = data.template_file.lseg_lambda_policy.rendered
}