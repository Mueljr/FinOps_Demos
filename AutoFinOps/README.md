# AutoFinOps: Automated AWS Cost & Tag Checker with Dashboard

A lightweight FinOps tool to automatically check compliance of AWS resources for required tags and generate a dashboard report. 

Also checks the cost of resources used so far, to guide in budgeting.

---

## 🚀 Objective

Many organizations enforce cost allocation and compliance by tagging cloud resources. Missing or incorrect tags can cause:

- Budgeting gaps
- Compliance issues
- Cost tracking inaccuracies
---

## ⚙️ Tech Stack

- **Python (Boto3)** – queries AWS APIs to list EC2 instances and tags
- **GitHub Actions** – automates pipeline execution and deployments
- **AWS S3** – stores the HTML dashboard
- **HTML/CSS** – basic dashboard generation
- **GitHub Secrets** – secures credentials without hardcoding

---

## 📁 Repo Structure

main.tf
    → Provisions:
         - S3 bucket for HTML dashboard
         - IAM user (finops-bot) + access keys
         - IAM policy for reading Cost Explorer, EC2, and tagging APIs
         - AWS budget alert (optional)
    → Outputs S3 website URL and IAM credentials

tag_checker.py
    → Checks EC2 instances for missing mandatory tags and logs results

budget_checker.py
    → Checks AWS Cost Explorer for services exceeding budget limits and logs findings

budget_checker_test.py
    → Simulates budget_checker.py logic for testing without live AWS calls

index.html
    → HTML dashboard that displays results of tag and budget checks

.github/workflows/main.yml
    → GitHub Actions pipeline that:
         - Runs both Python checks
         - Uploads dashboard file to S3 bucket

