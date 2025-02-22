# About

This project is a continuation of the [finops-tech-challenge](https://github.com/vxmm/finops-tech-challenge) designed to provide an infrastructure implementation in AWS. It adheres to standards of flexibility, reusability and reliability using known software design patterns, including modular and design and separated pipelines for infrastructure and code deployment.

# Changes to integrate with Lambda

For a detailed explanation on the Python code utilised, see my [other project](https://github.com/vxmm/finops-tech-challenge). Major changes for integration with Lambda involve the following: 

* only processing 1 file at a time based on the S3 PUT event in a particular bucket
* as we are processing objects instead of files, we are no longer abiding by the directory level requirements & verification
* error logs and variables are now hard-coded
* end user no longer maintains any input on variables or paths, these will be maintained in the code releases
* replaced with more graceful termination using return None instead of exit()

# Lambda + S3

To integrate our Python project with AWS Lambda with minimal changes, I've opted to utilise the following workflow and use the native Lambda's /tmp/ storage to process the .csv files:

![image](https://github.com/user-attachments/assets/538a55f8-0b50-41d8-8ea4-99188da25aa2)

# Terraform

To manage the infrastructure, I've opted to utilise Terraform in order to provision the following resources:

![image](https://github.com/user-attachments/assets/7b8d35e5-d577-4dbe-a5db-d8eb76dddb1b)

# GitHub Actions + OpenID

In order to authorise changes in the infrastructure, I've configured AWS to trust GitHub's OIDC as a federated identity instead of storing AWS credentials directly.

See GitHub's [official documentation](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) and this [detailed AWS example guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#links) on how to implement these changes in your AWS account.

![image](https://github.com/user-attachments/assets/3d505bba-3ac2-4974-8f40-6f88ec514767)

# Deployment Workflows

Since the project is rather basic, we keep the infrastructure and code release pipelines separated within the same repo. An update to the python code pushes the artifact to the corresponding S3 bucket, whereas an update to the infrastructure code triggers a Terraform build. These two behaviors are integrated in the 2 Workflows attached to the project. 

![image](https://github.com/user-attachments/assets/7b045401-4d13-4bb9-856c-5d51e67cd4d2)

# Validation 

We perform a few validations before deployment into infrastructure, namely that: 

* the name of the S3 input bucket matches the hardcoded value "project-stocks-vxmm" so it doesn't accidentally source other buckets when deploying 
* the name of the S3 output bucket matches the prescriptive value "project-stocks-vxmm-${current_region}" so it doesn't provision new buckets
* the region name is consistent across all references in modules and main variables.tf - this is not too much of a concern for IAM since it's a global service and we're not doing multi-region deployments but it's a good idea to have this sort of check regardless 
