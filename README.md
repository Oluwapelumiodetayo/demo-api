# Demo API — Containerised FastAPI + Postgres (AWS DevOps Project)

## Overview

This project is a production-style containerised FastAPI application built as part of a DevOps learning journey. It demonstrates how to build, containerise, and run a multi-service system using Docker and Docker Compose, and how to deploy static web assets to AWS S3.

The stack includes:

* FastAPI backend API
* PostgreSQL database
* Docker multi-stage build
* Docker Compose orchestration
* AWS S3 static hosting
* AWS CloudFront distribution (CDN)

---

## Architecture

Local Development:
FastAPI API  →  PostgreSQL (Docker container)

Production Deployment:
Astro build → AWS S3 → CloudFront CDN → Public HTTPS website

---

## API Endpoints

| Method | Endpoint         | Description                   |
| ------ | ---------------- | ----------------------------- |
| GET    | /health          | Service health check          |
| GET    | /regions         | Lists AWS EC2 regions         |
| GET    | /tokens?length=N | Generates secure random token |
| GET    | /db              | Tests PostgreSQL connection   |

---

## How to Run Locally (Docker)

### 1. Clone repository

git clone https://github.com/Oluwapelumiodetayo/aws-astro-blog.git
cd demo-api

### 2. Build and start services

docker compose up --build

### 3. Test API

http://localhost:8080/docs

or

curl http://localhost:8080/health
curl http://localhost:8080/db

---

## Docker Setup

### Build image

docker build -t demo-api .

### Run container

docker run -p 8080:8080 demo-api

### Check running containers

docker ps

---

## AWS Deployment (Static Website)

### S3 Deployment

* Built static Astro site using `npm run build`

* Synced output folder to S3 bucket:
  aws s3 sync ./dist s3://my-astro-blog-oluwapelumi-2026

* Enabled S3 Static Website Hosting

* Configured index document: index.html

### CloudFront CDN

* Created CloudFront distribution using S3 website endpoint
* Enabled global CDN caching
* Served site via HTTPS CloudFront domain

---

## Key DevOps Concepts Demonstrated

* Containerisation using Docker (multi-stage builds)
* Service orchestration using Docker Compose
* Environment isolation with containers
* Microservice communication (API ↔ DB)
* Infrastructure as a Service (AWS S3)
* Content Delivery Network (CloudFront)
* Static website hosting architecture
* Build reproducibility and deployment automation

---

## Project Structure

demo-api/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── test_main.py
└── README.md

---

## What I Learned

* How to containerise a FastAPI application
* How to connect multiple services using Docker Compose
* How to deploy static websites to AWS S3
* How CloudFront improves performance and security
* How production systems are structured in real environments

---

## Next Steps

* Deploy API to AWS ECS Fargate
* Add CI/CD pipeline using GitHub Actions
* Add monitoring with CloudWatch
* Add authentication layer (JWT)

