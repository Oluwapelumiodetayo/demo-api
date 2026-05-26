ECS Fargate Deployment Report — Demo API (Production Simulation)

## Overview

This document describes the full deployment of a containerised FastAPI application using AWS ECS Fargate and Amazon ECR, upgraded with Application Load Balancer (ALB) for production-style routing.

The goal was to simulate a real-world DevOps pipeline:

Docker Image → Amazon ECR → ECS Fargate → Application Load Balancer → Public API Access

---

## Live Public API (Production Endpoint)

Base URL (ALB DNS):

http://demo-alb-361957588.us-east-1.elb.amazonaws.com

### Working Endpoints

Health Check:
http://demo-alb-361957588.us-east-1.elb.amazonaws.com/health

Token Generator:
http://demo-alb-361957588.us-east-1.elb.amazonaws.com/tokens

Test Results:

curl http://demo-alb-361957588.us-east-1.elb.amazonaws.com/health
Response:
{"status":"ok"}

curl http://demo-alb-361957588.us-east-1.elb.amazonaws.com/tokens
Response:
{"token":"bePY3TzbCRY-yg2rYq1DlRWhzXaQ38vlVFaphoGwqY8"}

---

## AWS Services Used

### 1. Amazon ECR (Elastic Container Registry)

- Image repository: demo-api
- Tag used: v1
- Image URI:
160823835026.dkr.ecr.us-east-1.amazonaws.com/demo-api:v1

Docker push confirmed:
- Layers uploaded successfully
- Image digest generated:
sha256:0ff49d5e7096162238ca6c754b75d2eec92517dafc4d8b2292673af4bb2600cc

---

### 2. Amazon ECS (Elastic Container Service)

- Cluster: demo-cluster
- Service: demo-svc
- Task Definition: demo-api:2
- Launch Type: AWS Fargate (serverless containers)

Task Configuration:
- CPU: 0.25 vCPU
- Memory: 0.5 GB
- Container port: 8080
- Execution role: ecsTaskExecutionRole

ECS Responsibilities:
- Pulled image from ECR
- Started container task
- Replaced failed tasks automatically
- Maintained service health

Current Status:
✔ Service deployed successfully
✔ Task running and healthy
✔ ALB health checks passing (/health = 200 OK)

---

### 3. Application Load Balancer (ALB)

- Name: demo-alb
- Scheme: Internet-facing
- Listener: HTTP :80
- Target Group: demo-tg

Function:
- Routes internet traffic to ECS tasks
- Performs health checks on /health
- Replaces failed targets automatically

---

### 4. Security Groups

ECS Task Security Group:
- Name: demo-task-sg
- Inbound rule:
  - Port: 8080
  - Source: ALB security group only (recommended)

ALB Security Group:
- Allows HTTP (80) from 0.0.0.0/0

---

### 5. Networking

- ECS tasks run in AWS VPC: 172.31.0.0/16
- Tasks are assigned networking via awsvpc mode
- ALB is public-facing
- ECS tasks are accessed only via ALB (no direct public dependency in final architecture)

---

## Architecture Flow

User Request → Internet → ALB → Target Group → ECS Fargate Task → FastAPI Container → Response

Deployment Flow:

Docker Build → Docker Push → Amazon ECR → ECS Task Pulls Image → Container Runs → ALB Routes Traffic → API Live

---

## Key DevOps Learnings

- Container image lifecycle management using Amazon ECR
- Serverless container orchestration using ECS Fargate
- Load balancing with ALB and target groups
- Health checks for service reliability (/health endpoint)
- Security group-based traffic control
- Production-style deployment validation using curl

---

## Verification Evidence

Successful deployment confirmed via:

curl /health
→ {"status":"ok"}

curl /tokens
→ Random secure token generated

ALB DNS reachable publicly:
✔ HTTP 200 responses
✔ Load balancer routing working
✔ ECS task healthy

---

## Cost & Safety Notes

- This is a learning / sandbox deployment
- ECS tasks and ALB incur AWS charges while running
- Always stop service when not testing:

Stop ECS Service:
- AWS Console → ECS → demo-svc → Update → Desired tasks = 0

OR delete service after testing

---

## Status Summary

✔ ECR Image pushed successfully
✔ ECS Fargate service running
✔ ALB configured and routing traffic
✔ Target group healthy
✔ Public API accessible
✔ End-to-end deployment successful

---

END OF DEPLOYMENT REPORT
