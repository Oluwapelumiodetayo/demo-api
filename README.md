# Demo API — Containerised FastAPI + Postgres (AWS DevOps Project)

## Overview

This project is a production-style, containerised FastAPI microservice built as part of a DevOps learning journey. It demonstrates how modern backend systems are designed, deployed, monitored, and operated using industry-standard AWS services and container orchestration.

The goal of this project was not just to build an API, but to simulate a real production system with proper deployment pipelines, load balancing, observability, and failure testing.

The system was fully deployed on AWS using ECS Fargate, exposed via an Application Load Balancer, and monitored using CloudWatch logging and alarms.

## Tech Stack

- FastAPI (Python backend)
- PostgreSQL (local development database)
- Docker (containerisation)
- Docker Compose (local orchestration)
- Amazon ECR (container registry)
- Amazon ECS Fargate (serverless containers)
- Application Load Balancer (traffic distribution)
- Amazon CloudWatch (logs, metrics, alarms)
- AWS SNS (alert notifications)

## System Architecture

Local Development:
FastAPI API → PostgreSQL (Docker container)

Production Architecture:
Docker Image → Amazon ECR → ECS Fargate Service → Application Load Balancer → Internet → CloudWatch Monitoring + Alerts

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Service health check |
| GET | /regions | Returns available AWS EC2 regions |
| GET | /tokens?length=N | Generates secure random token |
| GET | /db | Tests PostgreSQL connectivity |

## Live Deployment

Base URL:
http://demo-alb-361957588.us-east-1.elb.amazonaws.com

Example:
curl http://demo-alb-361957588.us-east-1.elb.amazonaws.com/health

## Local Development Setup

Build image:
docker build -t demo-api .

Run container:
docker run -p 8080:8080 demo-api

Access:
http://localhost:8080/docs

## AWS Deployment Workflow

Step 1: Build and push image to ECR
docker tag demo-api:v5 160823835026.dkr.ecr.us-east-1.amazonaws.com/demo-api:v5
docker push 160823835026.dkr.ecr.us-east-1.amazonaws.com/demo-api:v5

Step 2: ECS Fargate Service Configuration
Cluster: demo-cluster
Service: demo-svc
Task Definition: demo-api:4
Launch Type: Fargate
CPU: 0.25 vCPU
Memory: 512 MB
Network Mode: awsvpc
Execution Role: ecsTaskExecutionRole

Step 3: Load Balancer Configuration
Type: Application Load Balancer
Target Group: demo-tg
Listener: HTTP :80
Health Check Path: /health
Traffic Routing: ECS service-backed targets

## Observability and Monitoring (CloudWatch)

This project implements production-grade observability using AWS CloudWatch.

Structured Logging:
Every API request is logged in JSON format with:
- HTTP method
- Endpoint path
- Status code
- Response time (ms)
- Correlation ID

Example:
{
  "level": "info",
  "event": "request",
  "method": "GET",
  "path": "/health",
  "status": 200,
  "duration_ms": 1.05,
  "correlation_id": "9b1358db-0ad7-4a4d-b2d8-03791946657e"
}

CloudWatch Logs Insights Query:
fields @timestamp, path, status, duration_ms
| filter event = "request"
| stats avg(duration_ms), pct(duration_ms, 99) by path
| sort avg(duration_ms) desc

CloudWatch Alarm:
Metric: HTTPCode_Target_5XX_Count
Threshold: > 5 errors
Evaluation period: 5 minutes
Action: SNS email notification

Failure Simulation:
A temporary /break endpoint was used to:
- Generate intentional 500 errors
- Trigger ALB 5xx metric spike
- Confirm CloudWatch alarm (OK → ALARM)
- Verify SNS email alerts
- Validate logs in CloudWatch Logs Insights

## Key DevOps Concepts Demonstrated

- Containerised application with Docker
- ECR image lifecycle management
- ECS Fargate serverless deployment
- Application Load Balancer routing
- CloudWatch logging and monitoring
- Log Insights performance analysis
- CloudWatch alarms with SNS alerts
- Production failure simulation and testing

## What I Learned

This project demonstrates a real production-style DevOps workflow from local development to cloud deployment.

Key learnings:
- ECS updates containers without downtime
- ALB routes only to healthy targets
- Structured logs simplify debugging
- CloudWatch turns logs into insights
- Production systems require observability + alerts

## Next Steps

- Add CI/CD with GitHub Actions
- Add JWT authentication
- Implement Terraform (Infrastructure as Code)
- Add CloudWatch dashboards
- Add distributed tracing (AWS X-Ray)
