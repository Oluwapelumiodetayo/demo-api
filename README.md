Demo API — Containerised FastAPI + Postgres (AWS DevOps Project)

## Overview

This project is a production-style containerised FastAPI application built as part of a DevOps learning journey. It demonstrates how to build, containerise, and deploy a microservice using Docker, Amazon ECR, and ECS Fargate with a load-balanced architecture.

The stack includes:

FastAPI backend API  
PostgreSQL database (local development)  
Docker multi-stage build  
Docker Compose orchestration  
AWS Elastic Container Registry (ECR)  
AWS ECS Fargate (serverless containers)  
Application Load Balancer (ALB)  

---

## Architecture

Local Development:
FastAPI API → PostgreSQL (Docker container)

Production Deployment:
Docker Image → ECR → ECS Fargate Task → ALB → Public Internet

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Service health check |
| GET | /regions | Lists AWS EC2 regions |
| GET | /tokens?length=N | Generates secure random token |
| GET | /db | Tests PostgreSQL connection |

---

## Live Production URL (AWS ECS + ALB)

Base URL:
http://demo-alb-361957588.us-east-1.elb.amazonaws.com

Test endpoints:
- /health
- /tokens
- /db

Example:
curl http://demo-alb-361957588.us-east-1.elb.amazonaws.com/health

---

## Docker Setup (Local)

Build image:
docker build -t demo-api .

Run container:
docker run -p 8080:8080 demo-api

Test locally:
http://localhost:8080/docs

---

## AWS Deployment (ECR + ECS Fargate)

### 1. Build and push image to ECR

docker tag demo-api:v1 160823835026.dkr.ecr.us-east-1.amazonaws.com/demo-api:v1

docker push 160823835026.dkr.ecr.us-east-1.amazonaws.com/demo-api:v1

---

### 2. ECS Fargate Service

- Cluster: demo-cluster  
- Service: demo-svc  
- Task Definition: demo-api:2  
- Execution Role: ecsTaskExecutionRole  
- Network Mode: awsvpc  
- CPU: 0.25 vCPU  
- Memory: 512 MB  

---

### 3. Load Balancer

- Type: Application Load Balancer  
- Name: demo-alb  
- Target Group: demo-tg  
- Listener: HTTP :80  
- Health Check: /health  

---

## Key DevOps Concepts Demonstrated

- Containerisation using Docker
- Image registry workflow using Amazon ECR
- Serverless containers with ECS Fargate
- Load balancing with ALB
- Health checks and service discovery
- Production-style deployment pipeline

---

## What I Learned

- How container images move from local → ECR → ECS
- How ECS tasks are replaced without downtime
- How ALB routes traffic to healthy tasks
- How IAM roles (ecsTaskExecutionRole) enable task execution
- How real production AWS architectures are structured

---

## Next Steps

- Add CI/CD with GitHub Actions  
- Add CloudWatch logging and alarms  
- Add authentication (JWT)  
- Move to HTTPS with ACM + Route53  

