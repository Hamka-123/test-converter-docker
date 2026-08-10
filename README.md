# Test Converter — Dockerized Application

A hands-on DevOps project focused on **Docker, application containerization, service configuration, and infrastructure automation**.

The project started as a practical exercise and evolved into a small multi-service environment for experimenting with containerized application infrastructure.

## 🎯 Goals

The project focuses on:

* Docker and containerization
* Running application and database services in isolated environments
* Infrastructure automation with Bash
* Environment configuration
* Service-to-service communication
* Technical documentation and architecture
* Iterative refactoring and improvement

## 🏗️ Architecture

The application consists of several containerized components:

```text id="h9g1ps"
                    ┌──────────────┐
                    │    Client    │
                    └───────┬──────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ Python HTTP  │
                    │    Server    │
                    └───────┬──────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   MariaDB    │
                    └───────┬──────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  phpMyAdmin  │
                    └──────────────┘
```

The architecture and implementation are documented in the [`docs`](./docs) directory.

## 🚀 Getting Started

### Requirements

* Docker
* Docker CLI
* Bash
* Git

Clone the repository:

```bash id="m3c7xy"
git clone https://github.com/Hamka-123/test-converter-docker.git
cd test-converter-docker
```

The project uses environment variables for configuration. See the project documentation and scripts for the required configuration.

### Run

Use the provided scripts to build and start the required services.

The exact workflow may evolve as the project develops.

---

## 📋 Project Planning

Development is tracked using a GitHub Project board:

**[Test Converter — Project Board](https://github.com/users/Hamka-123/projects/2)**

The board is used to break the work into tasks, track progress, and plan further improvements.

This project follows an iterative approach:

```text id="7aqh0x"
Plan
  ↓
Implement
  ↓
Test
  ↓
Refactor
  ↓
Document
  ↓
Improve
```

## 🔧 Technologies

* Python
* Bash
* Docker
* MariaDB
* phpMyAdmin

## 📚 Documentation

Additional technical documentation, architecture notes, and development materials are available in [`docs`](./docs).

## 📌 Status

This is an **active hands-on DevOps project**.

The implementation and infrastructure are intentionally evolving as new requirements and improvements are introduced.

---

> This repository is part of my ongoing hands-on work to deepen my practical engineering skills in DevOps, infrastructure, and automation.
