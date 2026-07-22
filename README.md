<h1 align="center">📘 Composio App Research Case Study</h1>

<p align="center">
  A lightweight agent-driven research pipeline for the 100-app audit
</p>

<p align="center">
  <a href="https://composio-assignment-flame.vercel.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live-Demo-2ea44f?style=for-the-badge" alt="Live Demo" />
  </a>
  <a href="https://github.com/aryan9855/ComposioAssignment" target="_blank">
    <img src="https://img.shields.io/badge/Source-Repo-181717?style=for-the-badge" alt="Source Repo" />
  </a>
</p>

---

## 🚀 Overview

This repository packages the final delivery for the AI Product Ops Intern take-home assignment:

- a single-page HTML case study deployed publicly
- a lightweight research-agent style Python pipeline
- a generated JSON artifact showing the normalized output for all 100 apps

The goal is to make the findings, workflow, confidence bands, and verification logic easy for a human reviewer to understand at a glance.

---

## 🧠 What’s inside

### Frontend / Deliverable
- `index.html` — polished single-page case study used for the public live demo
- `research_output.json` — generated research summary artifact for the audited app set

### Agent / Pipeline
- `research_agent.py` — deterministic research script that classifies the app list by category, auth posture, and buildability signal

### Submission Access
- Live demo: https://composio-assignment-flame.vercel.app/
- Source repo: https://github.com/aryan9855/ComposioAssignment

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

This repo is designed to support the final submission requirements with a clear handoff:

- a live public case-study URL
- a reproducible research pipeline
- a short README explaining how to rerun the agent and inspect the result

> The deployed HTML page is now available at the live demo URL above, while the local preview remains useful for offline reruns and development.
