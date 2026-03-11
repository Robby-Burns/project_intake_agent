# 🔧 System Maintenance & Handoff Guide

**Project:** ProjectIntakeAgentThree
**Version:** 1.5.0
**Framework:** 10-Part AI Agent Framework

---

## 🔑 Financial Ownership & API Keys
*   **OpenAI API Key:** Owned by [CLIENT NAME]. Billed monthly.
*   **Azure/Microsoft Graph:** Owned by [CLIENT IT]. Used for SharePoint/Planner integration.
*   **Hosting:** Docker Container (AWS ECS / Azure Container Apps).
*   **Database:** PostgreSQL (AWS RDS / Azure Database for PostgreSQL).

## 🔄 Model Deprecation Plan
This system uses Agnostic Factories to avoid vendor lock-in. If a model (e.g., `gpt-4o`) is deprecated:
1.  **Do NOT edit code.**
2.  **Edit `config/scale.yaml`:**
    ```yaml
    llm:
      primary:
        model: "gpt-4o-new-version"
    ```
3.  **Deploy:** The factory (`app/factories/llm_factory.py`) will automatically pick up the new configuration.

## 📅 Audit Schedule (Mandatory)
*   **Frequency:** Bi-Annual (March & September).
*   **Trigger:** Automated cron job calls `POST /audit/run`.
*   **Process:**
    1.  System generates a report (`docs/audits/AUDIT_REPORT_YYYY-MM-DD.md`).
    2.  Notification sent to configured channel (Slack/Email).
    3.  Human Reviewer approves/rejects findings.
    4.  Approved changes are applied.

## 🚨 Emergency Contacts & Troubleshooting
*   **If the Agent Hallucinates:**
    *   Check `logs/app.log` for recent prompts.
    *   Adjust `temperature` in `config/scale.yaml`.
*   **If the Agent Freezes:**
    *   Restart the container: `docker-compose restart`.
    *   Check database connectivity.
*   **If Costs Spike:**
    *   Check the `cost_controls` block in `scale.yaml`.
    *   Lower the `alert_threshold_usd`.

## 🛡️ Kill Switch Procedure
To immediately stop all external API calls (OpenAI, Jira, etc.):
1.  **Edit `config/scale.yaml`:** Set `risk_score: 17`.
2.  **Redeploy/Restart:** The application will enter "Emergency Mode" and block all outbound traffic.
