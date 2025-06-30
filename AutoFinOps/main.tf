terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Random suffix so bucket names are unique
resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "dashboard" {
  bucket = "autofinops-dashboard-${random_id.suffix.hex}"

  tags = {
    Name = "FinOps Dashboard"
  }
}

resource "aws_iam_user" "finops_bot" {
  name = "finops-bot"
}

resource "aws_iam_user_policy" "finops_policy" {
  name = "finops-policy"
  user = aws_iam_user.finops_bot.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "budgets:ViewBudget",
          "ce:GetCostAndUsage",
          "ec2:Describe*",
          "s3:List*",
          "tag:GetResources"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_access_key" "finops_key" {
  user = aws_iam_user.finops_bot.name
}

resource "aws_budgets_budget" "monthly_budget" {
  name              = "FinOpsMonthlyBudget"
  budget_type       = "COST"
  limit_amount      = "1"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    notification_type          = "ACTUAL"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    subscriber_email_addresses = ["your@email.com"]
  }
}

output "dashboard_url" {
  value = "http://${aws_s3_bucket.dashboard.bucket}.s3-website-us-east-1.amazonaws.com"
}

output "aws_access_key_id" {
  value     = aws_iam_access_key.finops_key.id
  sensitive = true
}

output "aws_secret_access_key" {
  value     = aws_iam_access_key.finops_key.secret
  sensitive = true
}