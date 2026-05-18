# ECS Fargate Deployment Report — Demo API

## Overview

This document describes the deployment of a containerised FastAPI application to AWS using ECS Fargate and Amazon ECR.

The goal was to simulate a production-style deployment pipeline:

Docker Image → Amazon ECR → ECS Fargate Task → Public Access via IP

---

## Live API URL

Public Base URL:

http://44.202.188.111:8080

Example endpoint:

/health → http://44.202.188.111:8080/health

Tested with:

curl http://44.202.188.111:8080/health

Response:

{"status":"ok"}

---

## AWS Services Used

### 1. Amazon ECR (Elastic Container Registry)

- Stored Docker image: demo-api:v1
- Image pushed from local machine using Docker CLI
- Acts as private container registry for ECS

Image reference:

160823835026.dkr.ecr.us-east-1.amazonaws.com/demo-api:v1

---

### 2. Amazon ECS (Elastic Container Service)

- Cluster name: demo-cluster
- Launch type: AWS Fargate (serverless containers)
- Task definition: demo-api:2

Configuration:
- CPU: 0.25 vCPU
- Memory: 0.5 GB
- Container port: 8080
- Execution role: ecsTaskExecutionRole

ECS automatically:
- Pulled image from ECR
- Started container
- Managed runtime lifecycle

---

### 3. Security Group

- Name: demo-task-sg
- Inbound rule:
  - TCP port 8080
  - Source: 0.0.0.0/0 (public access for testing)

---

### 4. Networking

- ECS task assigned a public IP
- Application exposed on port 8080
- Verified using curl from local machine

---

## Architecture Flow

Docker Build → Docker Push → Amazon ECR → ECS Task Pulls Image → Container Runs → Public IP Assigned → API Accessible

---

## Key Learnings

- How container images are stored in Amazon ECR
- How ECS Fargate runs containers without managing servers
- How task definitions control compute resources
- How security groups expose services safely
- How to validate deployment using curl

---

## Verification

Deployment confirmed with:

curl http://44.202.188.111:8080/health

Output:

{"status":"ok"}

---

## Notes

- This is a public test deployment (not production-secure)
- Port 8080 is exposed for learning purposes only
- Tasks should be stopped after testing to avoid cost

---

## Status

✔ ECR Image pushed  
✔ ECS Task running  
✔ Public endpoint accessible  
✔ Health check successful  

END OF DEPLOYMENT
