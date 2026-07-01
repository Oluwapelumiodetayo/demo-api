# Demo API — Production Style FastAPI + PostgreSQL (AWS DevOps Project)

## Overview

This project is a production-style FastAPI application built to demonstrate modern DevOps and cloud engineering practices.

Rather than simply building an API, the focus of this project was to implement real-world operational concepts including containerisation, cloud deployment, observability, secure secret management, database credential rotation, and security scanning.

The application is built with FastAPI and PostgreSQL, containerised with Docker, and integrates multiple AWS services to simulate production engineering workflows.

---

## Technologies Used

- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Amazon ECS Fargate
- Amazon ECR
- Application Load Balancer
- AWS Secrets Manager
- AWS CloudTrail
- Amazon CloudWatch
- Amazon SNS
- Git
- Gitleaks

---

## Features

- Containerised FastAPI application
- PostgreSQL integration
- Health monitoring endpoint
- Secure random token generation
- AWS EC2 region discovery
- Database connectivity verification
- Structured JSON logging
- Secure database credential retrieval from AWS Secrets Manager
- CloudTrail auditing for secret access
- Manual database password rotation
- Git history secret scanning using Gitleaks

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /health | Service health check |
| GET | /regions | Returns available AWS regions |
| GET | /tokens?length=N | Generates secure random tokens |
| GET | /db | Verifies PostgreSQL connectivity |

---

# Local Development

Clone the repository.

```bash
git clone https://github.com/Oluwapelumiodetayo/demo-api.git
cd demo-api
```

Build the containers.

```bash
docker compose build
```

Start the application.

```bash
docker compose up -d
```

Open:

```
http://localhost:8080/docs
```

---

# Docker Architecture

```
FastAPI
      │
      ▼
get-secret.sh
      │
      ▼
AWS Secrets Manager
      │
      ▼
DATABASE_URL
      │
      ▼
PostgreSQL
```

The application retrieves its database credentials from AWS Secrets Manager during startup instead of storing passwords inside the application.

---

# AWS Deployment

The project demonstrates deployment using:

- Amazon Elastic Container Registry (ECR)
- Amazon ECS Fargate
- Application Load Balancer
- Amazon CloudWatch Logs
- Amazon SNS
- AWS Secrets Manager
- AWS CloudTrail

---

# Secure Secret Management

One objective of this project was to eliminate hardcoded database credentials.

Instead of storing passwords in Docker environment variables, the application:

1. Retrieves the database password from AWS Secrets Manager during startup.

2. Constructs the DATABASE_URL dynamically.

3. Starts the FastAPI application using the retrieved secret.

Application startup confirms this process:

```
DATABASE_URL loaded from Secrets Manager.
```

AWS CloudTrail records every `GetSecretValue` request, providing a complete audit trail without exposing the secret value.

---

# Database Password Rotation

This project also demonstrates manual secret rotation.

Rotation process:

1. Update the PostgreSQL user password.

2. Store the new password as a new version in AWS Secrets Manager.

3. Make the new version the current secret.

4. Restart the application.

5. Verify successful database connectivity using the new credential.

This follows the same rotation workflow commonly used in production environments.

---

# Observability

The application produces structured JSON logs containing:

- HTTP method
- Endpoint
- Status code
- Response time
- Correlation ID

Example:

```json
{
  "level":"info",
  "event":"request",
  "method":"GET",
  "path":"/health",
  "status":200,
  "duration_ms":1.24,
  "correlation_id":"..."
}
```

CloudWatch Logs Insights can be used to analyze application performance and request patterns.

---

# Security

Repository security was validated using Gitleaks.

During development:

- Initial scan detected 193 potential secret leaks.
- Investigation showed 192 were false positives originating from third-party libraries.
- One genuine API token was identified.
- The token was removed.
- Git history was rewritten using `git filter-repo`.
- The repository was verified to ensure the leaked credential was no longer recoverable.

This demonstrates secure secret remediation rather than simply deleting exposed files.

---

# DevOps Concepts Demonstrated

- Docker containerisation
- Docker Compose orchestration
- Amazon ECR image management
- ECS Fargate deployments
- Application Load Balancer routing
- Structured logging
- CloudWatch monitoring
- AWS Secrets Manager integration
- CloudTrail auditing
- Database credential rotation
- Git history rewriting
- Secret scanning with Gitleaks

---

# What I Learned

Through this project I gained practical experience with:

- Building containerised backend applications
- Deploying workloads on AWS
- Managing application secrets securely
- Rotating database credentials safely
- Auditing secret access using CloudTrail
- Monitoring applications with CloudWatch
- Detecting and remediating leaked secrets
- Applying production-oriented DevOps practices

---

# Future Improvements

- CI/CD using GitHub Actions
- Infrastructure as Code with Terraform
- JWT Authentication
- CloudWatch Dashboards
- AWS X-Ray distributed tracing
- Automatic Secrets Manager rotation with Lambda
