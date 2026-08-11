# gitlab-ai-content-engine
AI-powered multi-agent engine that transforms technical changes, code diffs, and product context into source-grounded, review-ready documentation and content.
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
flowchart LR
    A["Technical Inputs<br/>Code changes • Notes • API specs • Existing docs"]
    B["Context Preparation<br/>Extract facts • Organize sources • Retrieve context"]
    C["AI Content Workflow<br/>Draft • Technical Review • Tone • Structure"]
    D["Review-Ready Draft<br/>Sources • Flags • Version"]
    E["Human Review<br/>Approve or Request Changes"]
    F["Publishing Preparation<br/>Export approved content"]

    A --> B --> C --> D --> E
    E -->|Changes requested| C
    E -->|Approved| F
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
flowchart LR
    I["Input Analysis"] --> C["Context Reader"]
    C --> W["Documentation Writer"]
    W --> R["Technical Reviewer"]
    R --> T["Tone Optimizer"]
    T --> S["Structure & Content Refinement"]
    S --> H["Human Review"]

    H -->|Revise| W
    H -->|Approve| P["Publishing Preparation"]
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
flowchart TB
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

```text
gitlab-ai-content-engine/
│
├── frontend/
│   └── ...                 # Web application
│
├── backend/
│   ├── agents/             # CrewAI agents and workflow
│   ├── retrieval/          # Context and vector retrieval
│   ├── api/                # Backend endpoints
│   ├── database/           # Database models / access
│   └── ...
│
├── data/                   # Local/sample content where applicable
├── docs/                   # Project documentation and README assets
├── tests/                  # Tests
├── .env.example            # Environment variable template
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd gitlab-ai-content-engine
```

### 2. Create the environment

Create and activate a Python virtual environment for the backend.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

Add the required values for the project's LLM and database configuration.

**Do not commit `.env` or API keys to GitHub.**

### 5. Start the application

Start the backend and frontend using the project's configured development commands.

> Keep the actual commands for each service in the project-specific setup documentation if the frontend/backend run independently.

---

## Configuration

The application uses environment variables for credentials and service configuration.

Typical configuration includes:

```text
GEMINI_API_KEY
GOOGLE_API_KEY
DATABASE_URL
```

The real values belong only in `.env`.

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

## Security

Never commit:

- API keys
- Database passwords
- Repository access tokens
- Private credentials
- Production `.env` files

Use environment variables and keep secrets on the server side.

---

## Status

🚧 **Active development**

The project is being developed as a multi-agent AI documentation workflow with source ingestion, retrieval, content generation, technical review, refinement, and human approval.

---

<p align="center">

**Technical Change → Context → AI Workflow → Human Review → Documentation**

</p>
