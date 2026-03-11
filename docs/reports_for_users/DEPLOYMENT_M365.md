# 🚀 Deployment Guide: M365 Integration (v1.5.0)

**Target Environment:** Azure / Microsoft 365
**Framework:** 10-Part AI Agent Framework (v1.5.0)
**Last Updated:** March 8, 2026

---

## 🏗️ Deployment Architecture

The **Project Intake Agent** is deployed as a single Docker container ("Modular Monolith") that runs both the FastAPI Backend (Audit System) and the Streamlit Frontend (UI).

**Components:**
1.  **Container App:** Runs the Docker image (`project-intake-agent:latest`).
2.  **Database:** Azure Database for PostgreSQL (Flexible Server).
3.  **Identity:** Azure AD App Registration (for SharePoint/Planner access).
4.  **Secrets:** Azure Key Vault (stores API keys and DB credentials).

---

## 📦 Container Build & Push

We follow a **Container-First** strategy. Do NOT deploy code directly.

### 1. Build the Image
```bash
# From project root
docker build -t project-intake-agent:v1.5.0 .
```

### 2. Push to Registry (ACR)
```bash
# Tag for Azure Container Registry
docker tag project-intake-agent:v1.5.0 myregistry.azurecr.io/project-intake-agent:v1.5.0

# Push
docker push myregistry.azurecr.io/project-intake-agent:v1.5.0
```

---

## ☁️ Azure Infrastructure (Terraform)

We use Terraform to define the infrastructure as code.

### 1. Define Resources (`main.tf`)
*   **Azure Container App:** Hosting the Docker image.
*   **PostgreSQL Flexible Server:** Persistent storage for conversation history.
*   **Key Vault:** Secure storage for `OPENAI_API_KEY`, `DATABASE_URL`, and `MS_CLIENT_SECRET`.

### 2. Configure Environment Variables
Set these in your Container App configuration:

*   `OPENAI_API_KEY`: `@Microsoft.KeyVault(SecretUri=...)`
*   `DATABASE_URL`: `@Microsoft.KeyVault(SecretUri=...)`
*   `PM_TOOL_TYPE`: `planner` (for Microsoft Planner integration)
*   `MS_CLIENT_ID`: Your Azure AD App ID.
*   `MS_TENANT_ID`: Your Azure AD Tenant ID.
*   `MS_CLIENT_SECRET`: `@Microsoft.KeyVault(SecretUri=...)`

---

## 🔗 M365 Integration (SharePoint & Planner)

### 1. App Registration
Create an Azure AD App Registration with the following **Graph API Permissions**:
*   `Sites.Selected` (Application): To upload PDF reports to a specific SharePoint site.
*   `Group.ReadWrite.All` (Application): To create tasks in Microsoft Planner.
*   `User.Read.All` (Application): To assign tasks to users.

### 2. SharePoint Setup
1.  Create a Document Library for "Project Intake Reports".
2.  Grant the App Registration **Write** access to this specific site via PowerShell:
    ```powershell
    Grant-PnPAzureADAppSitePermission -AppId "YOUR_APP_ID" -DisplayName "Project Intake Agent" -Site "https://yourtenant.sharepoint.com/sites/ProjectIntake" -Permissions Write
    ```

### 3. Planner Setup
1.  Create a "Project Intake" Plan in Microsoft Planner.
2.  Note the `Plan ID` and set it as an environment variable `MS_PLAN_ID`.

---

## 🛡️ Kill Switch & Maintenance

### Emergency Stop
If the agent misbehaves:
1.  Update the Container App environment variable: `RISK_SCORE=17`.
2.  Restart the revision.
3.  The agent will enter "Emergency Mode" and block all outbound API calls.

### Audit Schedule
The system is configured to run a bi-annual security audit. Ensure a scheduled job (Azure Logic App or Container Job) calls the audit endpoint:
*   **Trigger:** First Monday of March & September.
*   **Action:** `POST https://your-app-url/audit/run`
