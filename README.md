# Apache Airflow 3: Hands-On Exploration & Data Engineering

![Airflow 3.0 Architecture](Airflow3.0.png)

## 📖 Project Overview
This repository documents my hands-on journey mastering **Apache Airflow 3**. It is based on the comprehensive curriculum **"The Complete Hands-On Introduction to Apache Airflow 3"** by Marc Lamberti.

The goal of this project was to move beyond basic DAG creation and explore advanced Data Engineering concepts, including **distributed architectures, custom plugin creation, data-aware scheduling (Assets), and scaling with Celery.**

## 🛠 Tech Stack
* **Orchestration:** Apache Airflow 3.0
* **Containerization:** Docker & Docker Compose
* **Database:** PostgreSQL
* **Language:** Python 3.12, SQL
* **Distributed Processing:** Celery Executor, Redis, Flower

## 📂 Repository Structure
Each folder in this repository represents a specific module or concept I implemented. Click the links below to view details and execution results for each:

| Folder | Description | Key Concepts |
| :--- | :--- | :--- |
| **[Postgresql_Airflow](./Postgresql_Airflow)** | **The Core ETL Pipeline** | PostgresOperator, Hooks, Sensors, SQL. |
| **[Assets](./Assets)** | **Data-Aware Scheduling** | Airflow Assets (Datasets), Event-driven triggers. |
| **[branching](./branching)** | **Conditional Logic** | `BranchPythonOperator`, decision trees. |
| **[celery_executor](./celery_executor)** | **Scaling & Distribution** | Celery, Workers, Queues, Redis, Flower. |
| **[tasks_grps](./tasks_grps)** | **UI Organization** | TaskGroups, Nested Groups, XComs data sharing. |
| **[creating_provider](./creating_provider)** | **Custom Extensibility** | Custom Operators, Decorators (`@task.sql`), Plugins. |

## 🏗 Architecture & Diagrams
Understanding the shift from Standard to Distributed Architecture:

### Distributed Architecture (Production Grade)
![Distributed Arch](Airflow3.0_distributed_arch.png)

### Airflow 2.0 vs 3.0 Concepts
![Airflow 2.0](Airflow2.0.png)

Airflow3.0 Single Node Architecture using docker:
![Airflow 3.0 Architecture](Airflow3.0.png)
