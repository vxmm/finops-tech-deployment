# About

This project is a continuation of the lseg-tech-challenge designed to provide an infrastructure implementation in AWS. It adheres to standards of flexibility, reusability and reliability using known software design patterns, including modular and design and separated pipelines for infrastructure and code deployment.

# Overview

For a detailed explanation on the Python code utilised, see here. It should be noted that an exact implementation into the infrastructure was
Python code changes

* only processing 1 file at a time based on the S3 PUT event in a particular bucket
* directory level verifications
* error logs and variables are now hard-coded
* any changes to these variables will be maintained in the code releases instead of the end user
* more graceful termination using return None instead of exit()

# Lambda + S3

To integrate our Python project with AWS Lambda with minimal changes, I've opted to utilise the following workflow and use the native Lambda's /tmp/ storage to process the .csv files:

![image](https://github.com/user-attachments/assets/538a55f8-0b50-41d8-8ea4-99188da25aa2)

# Terraform

To manage the infrastructure, I've opted to utilise Terraform in order to provision the following resources:

![image](https://github.com/user-attachments/assets/7b8d35e5-d577-4dbe-a5db-d8eb76dddb1b)

# GitHub Actions + OpenID

In order to authorise changes in the infrastructure, we have opted to configure AWS to trust GitHub's OIDC as a federated identity instead of storing AWS credentials directly.

See GitHub's [official documentation](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) and this [detailed AWS example guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#links) on how to implement these changes in your AWS account.

![image](https://github.com/user-attachments/assets/3d505bba-3ac2-4974-8f40-6f88ec514767)

# Deployment Workflows

Ideally, we would like to keep the infrastructure and code release pipelines separated

![image](https://github.com/user-attachments/assets/7b045401-4d13-4bb9-856c-5d51e67cd4d2)
