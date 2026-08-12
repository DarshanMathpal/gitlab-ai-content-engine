# GitLab AI Content & Documentation Engine

> Turn technical changes into source-grounded, review-ready documentation with a multi-agent AI workflow.

## Overview

The **GitLab AI Content & Documentation Engine** helps teams transform technical inputs such as code changes, release notes, API specifications, issue context, and existing documentation into structured content drafts.

Instead of asking one AI agent to generate everything at once, the system separates the work into focused stages:

**Context → Draft → Technical Review → Tone & Structure → Human Review → Publish**

The goal is simple: **reduce documentation effort without removing technical and editorial control.**

---

## Why this project?

Technical changes often arrive before their documentation is ready. Engineers may have the code change, product teams may have release context, and writers may have existing documentation — but that information is spread across different sources.

This project brings those inputs together and creates a controlled path from technical change to review-ready content.

### What it helps with

- Converting technical changes into documentation drafts
- Keeping generated content grounded in supplied source material
- Reusing relevant existing documentation and knowledge
- Separating technical validation from writing and tone refinement
- Keeping a human reviewer in the approval loop
- Maintaining draft/version context throughout the workflow

---

## How it works

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontSize": "11px"
  },
  "flowchart": {
    "nodeSpacing": 20,
    "rankSpacing": 25,
    "padding": 5
  }
}}%%

flowchart TD

    A["Technical Inputs<br/>Code changes • Notes • API specs • Existing docs"]
    B["Context Preparation<br/>Extract facts • Organize sources • Retrieve context"]
    C["AI Content Workflow<br/>Draft • Technical Review • Tone • Structure"]
    D["Review-Ready Draft<br/>Sources • Flags • Version"]
    E["Human Review<br/>Approve or Request Changes"]
    F["Publishing Preparation<br/>Export approved content"]

    A --> B
    B --> C
    C --> D
    D --> E
    E -->|Changes requested| C
    E -->|Approved| F

    classDef stage fill:#EEF2FF,stroke:#6366F1,color:#1E1B4B,stroke-width:1px;
    classDef review fill:#FEF3C7,stroke:#F59E0B,color:#78350F,stroke-width:1px;
    classDef output fill:#ECFDF5,stroke:#10B981,color:#064E3B,stroke-width:1px;

    class A,B,C stage;
    class E review;
    class D,F output;
```

### Typical input

A content request can combine:

- Code changes / diffs
- Release or product notes
- API specifications
- Issue or feature context
- Existing documentation
- Content type and audience requirements

### Typical output

Depending on the request, the workflow can prepare:

- Release notes
- Technical documentation
- Developer-facing blogs
- Onboarding content
- API documentation

---

## Multi-Agent Workflow

Each stage has a focused responsibility instead of relying on a single generation step.

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontSize": "11px"
  },
  "flowchart": {
    "nodeSpacing": 20,
    "rankSpacing": 25,
    "padding": 5
  }
}}%%

flowchart TD

    I["Input Analysis"]
    C["Context Reader"]
    W["Documentation Writer"]
    R["Technical Reviewer"]
    T["Tone Optimizer"]
    S["Structure & Content Refinement"]
    H["Human Review"]
    P["Publishing Preparation"]

    I --> C
    C --> W
    W --> R
    R --> T
    T --> S
    S --> H
    H -->|Revise| W
    H -->|Approve| P

    classDef stage fill:#EEF2FF,stroke:#6366F1,color:#1E1B4B,stroke-width:1px;
    classDef review fill:#FEF3C7,stroke:#F59E0B,color:#78350F,stroke-width:1px;
    classDef output fill:#ECFDF5,stroke:#10B981,color:#064E3B,stroke-width:1px;

    class I,C,W,R,T,S stage;
    class H review;
    class P output;
```

| Stage | Responsibility |
|---|---|
| **Context Reader** | Understands the supplied material, extracts relevant facts, and identifies missing context. |
| **Documentation Writer** | Creates the first structured draft using the prepared context. |
| **Technical Reviewer** | Checks whether technical claims remain supported by the available source material. |
| **Tone Optimizer** | Adjusts language for the selected audience and content type. |
| **Refinement** | Improves structure, clarity, headings, examples, and overall readability. |
| **Human Review** | Final review and approval before publishing. |

---

## Architecture

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontSize": "11px"
  },
  "flowchart": {
    "nodeSpacing": 20,
    "rankSpacing": 25,
    "padding": 5
  }
}}%%

flowchart TD

    subgraph UI["Application"]
        Intake["Content Intake"]
        Context["Context Review"]
        Workflow["Workflow Monitor"]
        Editor["Draft Editor"]
        Review["Review"]
    end

    subgraph API["Backend"]
        Jobs["Content Job Management"]
        Assembly["Context Assembly"]
        Orchestration["Agent Orchestration"]
        Versions["Draft & Version Management"]
    end

    subgraph AI["AI & Knowledge"]
        Retrieval["Retrieval / Knowledge"]
        Agents["CrewAI Agents"]
        LLM["LLM"]
    end

    subgraph Storage["Storage"]
        SQL["PostgreSQL / Supabase"]
        Vector["Chroma / Vector Store"]
    end

    Intake --> Jobs
    Context --> Assembly
    Workflow --> Orchestration
    Editor --> Versions
    Review --> Versions

    Jobs --> Assembly
    Assembly --> Retrieval
    Retrieval --> Vector
    Assembly --> Orchestration
    Orchestration --> Agents
    Agents --> LLM
    Agents --> Versions
    Versions --> SQL

    classDef stage fill:#EEF2FF,stroke:#6366F1,color:#1E1B4B,stroke-width:1px;
    classDef review fill:#FEF3C7,stroke:#F59E0B,color:#78350F,stroke-width:1px;
    classDef output fill:#ECFDF5,stroke:#10B981,color:#064E3B,stroke-width:1px;

    class Intake,Context,Workflow,Editor,Jobs,Assembly stage;
    class Review,Orchestration,Agents review;
    class Retrieval,LLM,Versions,SQL,Vector output;
```

### Architecture responsibilities

**Frontend / UI**
- Collects content requests and source files
- Displays context and workflow progress
- Provides the draft and review experience

**Backend**
- Handles content jobs and inputs
- Builds the context package
- Coordinates the agent workflow
- Stores draft/version information

**AI layer**
- Runs specialized content agents
- Uses retrieved context when relevant
- Produces structured intermediate and final outputs

**Knowledge / Retrieval**
- Makes existing documentation, terminology, examples, and other approved context searchable

**Database**
- Stores operational records such as jobs, drafts, sources, review information, and workflow state

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI |
| **AI Orchestration** | CrewAI |
| **LLM** | Gemini |
| **Retrieval / Vector Store** | Chroma |
| **Operational Database** | PostgreSQL / Supabase |
| **ORM / Database Access** | SQLAlchemy |
| **Configuration** | Python `.env` configuration |
| **Frontend** | Project web interface |

> The exact frontend/deployment configuration can vary with the environment. Backend and AI components above reflect the project's implementation direction.

---

## Project Structure

The repository is organized around the major application responsibilities rather than placing the entire workflow in a single module.

```text
gitlab-ai-content-engine/
│
├── backend/
│   ├── agents/
│   │   └── crew.py              # Multi-agent workflow
│   ├── retrieval/
│   │   └── chroma_store.py      # Vector retrieval
│   ├── auth/                    # Authentication-related logic
│   ├── database/                # Database configuration / models
│   ├── services/                # Application services
│   ├── chroma_data/             # Retrieval data where used
│   ├── main.py                  # FastAPI application entry point
│   ├── models.py                # Application models
│   └── requirements.txt         # Backend dependencies
│
├── frontend/
│   └── ...                      # Web application
│
├── data/
│   ├── sample_inputs/           # Example technical inputs
│   ├── sample_docs/             # Example documentation
│   ├── style_guides/            # Writing/style context
│   └── content_templates/       # Content templates
│
├── tests/
│   ├── functional_tests/
│   ├── ai_output_tests/
│   └── edge_cases/
│
├── docs/
│   └── readme_assets/            # README diagrams
│
├── .env.example
└── README.md
```

> Folder names can vary slightly with the current implementation; the structure above reflects the main responsibilities of the project.

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd gitlab-ai-content-engine
```

### 2. Create the backend environment

Create and activate a Python virtual environment for the backend.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

Configure the required LLM, GitLab, SMTP, and database variables.

**Do not commit .env, API keys, passwords, or access tokens to GitHub.**

### 5. Load the knowledge base

Index the knowledge base for retrieval

```bash
python -m retrieval.ingest_knowledge
```

### 6. Start the Backend

Start the FastAPI backend from the `backend` directory:

```bash
python3 -m uvicorn main:app --reload
```

Once the server starts, you can access:

| Service | Local URL |
|---|---|
| **Backend API** | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| **Interactive API Docs** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |

> The API documentation is provided by FastAPI's interactive Swagger interface.


### 7. Start the Frontend

Open a **new terminal** from the project root and start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Once the development server starts, you can access:

| Service | Local URL |
| --- | --- |
| **Frontend Application** | [http://localhost:3000](http://localhost:3000) |

> If the frontend dependencies have already been installed, you can skip `npm install` and run `npm run dev`.


### Running the Application

With both services running:

```text
Frontend
   │
   │  HTTP Requests
   ▼
FastAPI Backend
   │
   ├── AI Agents
   ├── Chroma Retrieval
   ├── Supabase / PostgreSQL
   └── GitLab Integration
```

Open the **frontend** to use the application.

Use the **FastAPI documentation** to inspect and test the backend API endpoints directly.

---

## Configuration

Create a local `.env` file using `.env.example`.

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Gemini API key used by the AI workflow |
| `GOOGLE_API_KEY` | Google API key where required by the configured AI services |
| `DATABASE_URL` | PostgreSQL / Supabase connection URL |
| `GITLAB_URL` | GitLab instance URL, for example `https://gitlab.com` |
| `GITLAB_TOKEN` | GitLab personal/project access token used for GitLab API access |
| `SMTP_HOST` | SMTP server hostname used for email delivery |
| `SMTP_PORT` | SMTP server port |
| `SMTP_USERNAME` | SMTP account username |
| `SMTP_PASSWORD` | SMTP account/app password |
| `SMTP_FROM` | Sender address used for application emails |

### Security

Keep real credentials only in `.env` or the deployment platform's secret manager.

**Never commit:**

- API keys
- Database passwords
- GitLab tokens
- SMTP passwords
- Production `.env` files

The `.env.example` file should contain variable names and safe placeholders only.

---

## Core Workflow in the Application

```mermaid
sequenceDiagram
    actor User
    participant UI as Application
    participant API as Backend
    participant R as Retrieval
    participant AI as Agent Workflow
    participant DB as Database

    User->>UI: Submit content request + sources
    UI->>API: Create content job
    API->>R: Prepare relevant context
    R-->>API: Retrieved context
    API->>AI: Start workflow
    AI->>AI: Read → Draft → Review → Refine
    AI-->>API: Draft + review signals
    API->>DB: Save draft/version
    API-->>UI: Show review-ready draft
    User->>UI: Review / request changes
    UI->>API: Approve or revise
    API->>DB: Save decision
```

---

## Source Grounding & Human Review

A central design principle is that generated content should remain connected to the supplied technical context.

The workflow therefore separates:

**source/context preparation → generation → technical checking → refinement → human approval**

This helps reduce unsupported claims and makes it easier for a reviewer to understand where the generated content came from.

AI generation is not treated as the final publishing decision.

---

## Example Use Case

### From code change to release documentation

```text
Code change / release context
            ↓
      Context preparation
            ↓
       Draft generation
            ↓
     Technical validation
            ↓
      Tone / structure
            ↓
        Human review
            ↓
      Approved content
```

A team can therefore start with technical information that already exists and use the engine to prepare a documentation draft rather than writing the entire document manually from scratch.

---

## Screenshots

### 1. Application Dashboard
[image]

### 2. Content Intake
[image]

### 3. AI Content Workflow
[image]

### 4. Generated Documentation
[image]

### 5. Human Review
[image]

---

## Development Notes

The project is organized around a clear separation of responsibilities:

- **Frontend** handles the user experience.
- **Backend** manages requests, data, and orchestration.
- **Agents** handle specialized content tasks.
- **Retrieval** supplies relevant existing knowledge.
- **Database** stores application state and versions.
- **Human review** controls the final approval step.

This separation makes the workflow easier to test, debug, and extend.

---

## Project Status

🚧 **Active development**

The project is being developed as a multi-agent AI documentation workflow with source ingestion, retrieval, content generation, technical review, refinement, and human approval.

---

## Contributors ⭐

This project was developed collaboratively by:

| Contributor | Role / Contribution |
|---|---|
| Himanshu Shende | Project Development |
| Himanshu Gupta | Project Development |
| Aparna Nale | Project Development |
| Mrunali Wadi | Project Development |
| Surya Rohila | Project Development |
| Darshan Mathpal | Project Development |

All contributors participated in the development, testing, documentation, and refinement of the project.

---

<p align="center">
  <strong>Technical Change → Context → AI Workflow → Human Review → Documentation</strong>
</p>
