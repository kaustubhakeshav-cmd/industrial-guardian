# Industrial Guardian SCADA

> An enterprise-grade Supervisory Control and Data Acquisition (SCADA) platform designed for real-time industrial telemetry monitoring and predictive maintenance.

## System Architecture

Industrial Guardian is built on a modern, decoupled microservices architecture deployed entirely via Docker. It ensures high-availability data ingestion and low-latency visualization for machine operators.

*   **Frontend (Telemetry Dashboard):** A high-performance React SPA built with Vite, utilizing Tailwind CSS for responsive UI components. It securely authenticates operators and visualizes real-time sensor streams.
*   **Backend (API & Auth):** An asynchronous FastAPI application handling secure JWT authentication, password hashing (`bcrypt`), and high-throughput data processing.
*   **Database (Persistence Layer):** A PostgreSQL relational database utilizing SQLAlchemy and `asyncpg` for non-blocking, high-speed read/write operations of time-series sensor data.

## Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, Node 20 | Client-side rendering and UI |
| **Backend** | Python 3.11, FastAPI, Uvicorn | RESTful API and WebSocket management |
| **Security** | PyJWT, Passlib, bcrypt | Operator authentication and authorization |
| **Database** | PostgreSQL, SQLAlchemy, asyncpg | Asynchronous data persistence |
| **Infrastructure** | Docker, Docker Compose | Containerization and environment parity |

## Local Development Setup

The entire infrastructure is containerized to ensure zero-configuration deployment across environments.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/kaustubhakeshava/industrial-guardian.git](https://github.com/kaustubhakeshava/industrial-guardian.git)
   cd industrial-guardian