# PeopleDesk AI
### AI-Powered Employee Self-Service Platform

**Simplifying everyday HR operations through Generative AI, intelligent assistance, and workflow automation.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red?logo=streamlit)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_AI-8E75B2)](https://ai.google.dev/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)](https://www.sqlite.org/)
[![Project Status](https://img.shields.io/badge/Status-Working_Prototype-success)]()

---

## Overview

PeopleDesk AI is an intelligent employee self-service platform designed to simplify routine Human Resource (HR) operations using Generative AI and application-level workflow automation.

In traditional workplace environments, employees often depend on HR teams for routine information such as leave policies, available leave balances, onboarding procedures, and application status updates. Managing these repetitive requests manually can increase administrative workload and delay access to information.

PeopleDesk AI addresses this challenge through a centralized platform that combines a conversational AI assistant with employee information management and HR workflows.

Employees can interact with the AI assistant, retrieve relevant information, submit leave applications, track request statuses, and monitor onboarding activities. HR administrators can review submitted leave applications and approve or reject pending requests through a dedicated dashboard.

The application integrates the Google Gemini API for natural-language assistance and SQLite for employee and leave-request data management.

## Problem Statement

Employees frequently face difficulties accessing routine HR services because information and processes are distributed across different communication channels and documents.

Common challenges include:

- Repetitive HR queries about policies and procedures.
- Limited visibility into available leave balances.
- Manual leave application and approval processes.
- Difficulty tracking submitted requests.
- Lack of centralized onboarding progress tracking.
- Repetitive administrative work for HR teams.

**Proposed Solution:** Build an AI-powered employee portal that provides conversational HR assistance, employee self-service features, and structured workflow management through a unified interface.

## Project Objectives

- Develop a centralized employee self-service platform.
- Integrate a Generative AI assistant for natural-language HR queries.
- Provide contextual AI responses using employee information and HR policies.
- Enable employees to submit and track leave applications.
- Provide HR administrators with leave approval and rejection functionality.
- Introduce an interactive employee onboarding tracker.
- Demonstrate the practical integration of AI with database-driven workflows.

## Key Features

### 1. AI HR Assistant

A conversational AI assistant powered by the Google Gemini API.

Employees can ask questions such as:

- What is my employee ID?
- How many leaves do I have remaining?
- What is the leave application policy?
- What documents are required during onboarding?
- What is the status of my leave request?

**How it works:**

1. The employee enters a question.
2. The application retrieves relevant employee information from SQLite.
3. Relevant sample HR policy content is selected using keyword-based retrieval.
4. The retrieved context is included in a prompt.
5. Google Gemini generates a contextual response.
6. The response is displayed in the chat interface.

### 2. Employee Dashboard

A centralized dashboard providing an overview of employee information and HR activities.

Features include:

- Employee profile information.
- Department and employee ID.
- Available leave balance.
- Recent leave-request activity.
- Leave utilization overview.
- Onboarding completion progress.
- Quick access to employee services.

### 3. Leave Balance Management

Employees can view their leave information through a dedicated dashboard.

The module displays:

- Total allocated leaves.
- Leaves utilized.
- Remaining leave balance.

The current demonstration uses sample employee records and a sample annual leave allocation.

### 4. Leave Application

Employees can submit leave requests through an interactive application form.

Features include:

- Leave start and end dates.
- Leave reason.
- Date-range validation.
- Remaining-balance validation.
- Automatic request ID generation.
- Database storage of submitted requests.

New applications are assigned a Pending status.

### 5. HR Admin Dashboard

A dedicated interface for demonstrating HR-side leave management.

HR administrators can:

- View all submitted leave applications.
- Review employee and leave details.
- Identify pending applications.
- Approve pending leave requests.
- Reject pending leave requests.
- View updated application statuses.

Approval and rejection actions update the corresponding records in SQLite.

### 6. Request Tracking

Employees can monitor their submitted leave applications.

Each request displays:

- Request ID.
- Submission date.
- Leave period.
- Reason for leave.
- Current application status.

Supported statuses:

- Pending
- Approved
- Rejected

### 7. Employee Onboarding Tracker

An interactive checklist that helps employees monitor their onboarding activities.

Example activities include:

- Document submission.
- Employee information verification.
- Account setup.
- Company policy review.
- Orientation completion.

Employees can mark tasks as completed and monitor their onboarding progress.

### 8. HR Knowledge Base

A centralized section containing sample HR policies and frequently asked questions.

It includes:

- Leave policies.
- Holiday policies.
- Employee onboarding guidelines.
- Employee support information.

The knowledge base also provides contextual information for the AI assistant.

---

## System Architecture

PeopleDesk AI follows a modular application architecture that connects the employee interface, Python application logic, AI service, and database.

**Application Flow:**

1. Employee or HR administrator accesses the Streamlit interface.
2. The interface sends the request to the Python application.
3. Python processes the request and identifies the required operation.
4. Relevant employee or leave information is retrieved from SQLite.
5. For AI queries, relevant context is passed to Google Gemini.
6. For leave workflows, Python performs database operations.
7. The application displays the generated response or updated information.

**Architecture Components:**

| Component | Responsibility |
|---|---|
| Streamlit | Interactive user interface |
| Python | Application logic and workflow management |
| Google Gemini API | Natural-language response generation |
| SQLite | Employee and leave-request storage |
| SQL | Database queries and updates |
| python-dotenv | Environment variable management |

## AI Integration and Workflow Logic

The AI assistant uses the Google Gemini API through the Python application.

### Context-Aware Response Generation

Instead of sending only the employee's question to the AI model, the application prepares relevant context.

This context can include:

- Employee identification details.
- Department information.
- Available leave balance.
- Existing leave requests.
- Relevant sample HR policy information.

The retrieved information is included in the prompt so Gemini can generate more relevant responses.

### Separation of AI and Backend Operations

An important design decision is the separation of conversational AI tasks from database operations.

| Operation | Implementation |
|---|---|
| Answer HR policy questions | Google Gemini API |
| Explain employee information | Gemini with retrieved context |
| Retrieve leave balance | Python and SQLite |
| Submit leave request | Python and SQLite |
| Approve or reject leave | Python and SQLite |
| Track request status | Python and SQLite |
| Update onboarding checklist | Streamlit session state |

This approach keeps important application operations deterministic instead of relying on AI-generated text to modify database records.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core application development |
| Streamlit | Frontend and interactive dashboard |
| Google Gemini API | Generative AI integration |
| SQLite | Relational database |
| SQL | Database operations |
| python-dotenv | Environment configuration |
| Git | Version control |
| GitHub | Source code hosting |

## Database Design

PeopleDesk AI uses SQLite as its lightweight relational database.

### Employees Table

Stores employee information.

| Field | Description |
|---|---|
| employee_id | Unique employee identifier |
| name | Employee name |
| department | Employee department |
| email | Employee email |
| leave_balance | Remaining leave balance |

### Leave Requests Table

Stores submitted leave applications.

| Field | Description |
|---|---|
| request_id | Unique leave request identifier |
| employee_id | Employee submitting the request |
| start_date | Leave start date |
| end_date | Leave end date |
| reason | Reason for leave |
| status | Current request status |
| created_at | Request creation timestamp |

The employee ID connects leave requests with employee records through a foreign-key relationship.

## Project Structure

```text
PeopleDesk_AI/
|
|-- streamlit_app.py       # Main Streamlit application
|-- database.py            # Database initialization and operations
|-- app.py                 # Original Flask application
|
|-- templates/
|   |-- index.html         # Original Flask interface
|
|-- static/
|   |-- style.css          # Original frontend styling
|   |-- script.js          # Original frontend scripts
|
|-- requirements.txt       # Python dependencies
|-- .gitignore             # Git exclusion rules
|-- .env                   # Local API credentials
|-- README.md              # Project documentation
|-- peopledesk.db          # Locally generated SQLite database
```

Note: The `.env`, `.venv`, and local database files are excluded from GitHub.

## Installation and Setup

### Prerequisites

- Python 3.10 or higher.
- Git.
- Google Gemini API key.
- Internet connection for Gemini API requests.

### Step 1: Clone the Repository

```bash
git clone https://github.com/SuhanaJena/PeopleDesk-AI.git
```

Navigate to the project directory:

```bash
cd PeopleDesk-AI
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment on macOS or Linux:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Gemini API Key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Generate an API key through Google AI Studio:

https://aistudio.google.com/apikey

**Security Note:** Never upload your actual API key to GitHub or share it publicly.

### Step 5: Run the Application

```bash
streamlit run streamlit_app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

## Functional Testing

The following scenarios describe the main functional behaviours of the prototype.

| Test Scenario | Expected Behaviour |
|---|---|
| Employee dashboard | Displays employee information |
| HR policy query | Generates a contextual AI response |
| Employee information query | Uses retrieved employee context |
| Leave balance check | Displays remaining leave balance |
| Valid leave application | Creates a Pending request |
| Invalid date range | Displays validation feedback |
| HR approval | Updates status to Approved |
| HR rejection | Updates status to Rejected |
| Request tracking | Displays current request status |
| Onboarding checklist | Updates task completion progress |

## Security and Current Limitations

PeopleDesk AI is an educational prototype and is not intended for production enterprise HR operations.

**Security considerations:**

- API credentials are stored in environment variables.
- `.env` is excluded from version control.
- Parameterized SQL queries are used for database operations.
- Demonstration employee information is fictional.

**Current limitations:**

- Uses sample employee data.
- HR Admin Dashboard does not currently implement authentication or role-based access control.
- Policy retrieval uses keyword matching rather than a full vector-based RAG pipeline.
- Onboarding checklist progress is maintained in Streamlit session state.
- Leave balance is not automatically deducted after approval.
- Leave calculations use calendar days and do not account for weekends or holidays.
- The application is not connected to an actual enterprise HRMS or payroll system.

## Future Enhancements

Potential improvements include:

- Role-based authentication for employees and HR administrators.
- Persistent onboarding progress using database storage.
- Automatic leave balance updates after approval.
- Advanced semantic search and Retrieval-Augmented Generation (RAG).
- AI agent tool calling for controlled application actions.
- Email notifications for leave status updates.
- Audit logs for administrative operations.
- Enterprise HRMS integration.
- Production database and cloud deployment.

## Developer

**Suhana Jena**

B.Tech in Computer Science and Engineering (Data Science)  
VIT-AP University

GitHub: [@SuhanaJena](https://github.com/SuhanaJena)

Project Repository: [PeopleDesk AI](https://github.com/SuhanaJena/PeopleDesk-AI)

---

**PeopleDesk AI — Bringing Conversational AI and Employee Workflows Together.**

Built using Python, Streamlit, Google Gemini API, and SQLite.