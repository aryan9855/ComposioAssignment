<h1 align="center">📘 Composio App Research Case Study</h1>

<p align="center">
  A lightweight agent-driven research pipeline for the 100-app audit
</p>

<p align="center">
  <a href="http://localhost:8000/index.html" target="_blank">
    <img src="https://img.shields.io/badge/Local-Preview-2ea44f?style=for-the-badge" alt="Local Preview" />
  </a>
  <a href="https://github.com/aryan9855/ComposioAssignment" target="_blank">
    <img src="https://img.shields.io/badge/Source-Repo-181717?style=for-the-badge" alt="Source Repo" />
  </a>
</p>

---

## 🚀 Overview

This repository packages the deliverable for the AI Product Ops Intern take-home assignment:

- a single self-explanatory HTML case-study page
- a lightweight research-agent style Python script
- a generated JSON artifact showing the normalized output for all 100 apps

The goal is to make the findings, workflow, agent logic, and verification evidence easy for both a human reviewer and another agent to consume.

---

## 🧠 What’s inside

### Frontend / Deliverable
- `index.html` — polished single-page case study
- `research_output.json` — generated research summary artifact

### Agent / Pipeline
- `research_agent.py` — deterministic research script that classifies the app list by category, auth posture, and buildability signal

---

## 📊 Core Findings

The page highlights the main patterns from the audit:

- OAuth2, API key, and token-based auth dominate the sample
- SaaS apps are largely self-serve or developer-trialable
- finance, ad, and research-heavy apps are more likely to be gated or partner-sensitive
- the easiest toolkit opportunities are public-doc-driven SaaS products with clear developer onboarding

---

## 🛠 Run locally

```bash
python research_agent.py
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
```

---

## 🔎 Verification Notes

The deliverable is intentionally transparent about confidence levels:

- high-confidence cases are clearly surfaced
- medium-confidence or policy-ambiguous apps are called out honestly
- the page shows the workflow and the verification loop, not just the final output

---

## 📁 Repo Structure

```text
ComposioAssignment/
├── index.html
├── research_agent.py
├── research_output.json
└── README.md
```

---

## 👨‍💻 Submission Summary

This repo is designed to support the final submission requirements:

- a local preview of the HTML case study
- a reproducible script for the research pipeline
- a short README that explains how to run the agent and inspect the results

> A public deployment URL can be added on top of this repo once you host the static page externally.
