# Cloud Operations Control Plane

> **Flagship CloudOps / Platform Engineering Project**

---

## Why I Built This

In most real AWS environments, the hard part isn’t *creating* resources — it’s **knowing what exists, what it’s costing, and whether it’s still needed**.

I built the **Cloud Operations Control Plane** to simulate the kind of **internal tooling** CloudOps and Platform Engineering teams rely on to keep cloud environments **visible, governed, and under control**.

This is **not an application**.
It’s a **cloud operations platform**.

---

## The Problem This Solves

As cloud usage grows, teams commonly run into:

* Limited visibility into deployed AWS resources
* Orphaned EBS volumes and snapshots causing silent cost leaks
* Manual, ad-hoc operational checks
* Weak audit trails for governance decisions

This project introduces a **safe, automated foundation** to address those operational gaps.

---

## How It Works (High Level)

```
EventBridge (Scheduled)
        │
        ▼
AWS Lambda (Inventory & Hygiene)
        │   IAM (Least Privilege)
        ▼
Amazon S3 (Versioned JSON Reports)
```

**Flow explained simply:**

* EventBridge runs the checks on a schedule
* Lambda collects inventory and hygiene data
* S3 stores the results as durable, auditable JSON reports

No servers. No cron jobs. No manual execution.

---

## What’s Implemented

### Phase 1 — Governance & Inventory ✅

This phase establishes a strong operational foundation:

* Terraform-managed AWS infrastructure with remote state and locking
* IAM + STS assume-role model (no long-lived credentials)
* Scheduled inventory collection using Lambda and EventBridge
* Inventory stored as time-stamped JSON in Amazon S3

**Resources inventoried:**

* EC2 instances
* EBS volumes
* EBS snapshots
* IAM users

---

### Phase 2 — Cost & Hygiene Automation ✅

This phase focuses on **real-world cost hygiene**:

* **Orphaned EBS volume detection**

  * Volumes not attached to any EC2 instance
* **Aged snapshot detection**

  * Snapshots older than 30 days

**Design choice:**

* Detection-only (no auto-deletion)
* All findings are written to S3 for auditability

This mirrors how production teams approach automation: **observe first, remediate later**.

---

## Repository Structure

```
cloud-operations-control-plane/
├── terraform/        # Infrastructure as Code
├── lambdas/          # Serverless automation logic
├── scripts/          # Local helper scripts
├── trust-policy.json # IAM trust relationship
└── README.md
```

---

## Technologies Used

* AWS Lambda
* Amazon EventBridge
* Amazon S3
* AWS IAM & STS
* Terraform
* Python (boto3)
* CloudWatch Logs

---

## Why This Project Matters

This project demonstrates:

* CloudOps / Platform Engineering mindset
* Governance-first automation
* Cost awareness and operational hygiene
* Safe, production-oriented design
* Practical Terraform and AWS workflows

The emphasis is on **operability**, not application features.

---

## Resume / Interview Summary

> Designed and implemented a Cloud Operations Control Plane using Terraform and AWS serverless services to automate AWS inventory and proactively detect cost-leaking resources through scheduled, auditable hygiene checks.

---

## Project Status

✅ **Intentionally complete at Phase 2**

The scope is deliberate: the project demonstrates how real CloudOps platforms are designed and operated without unnecessary complexity.

---
