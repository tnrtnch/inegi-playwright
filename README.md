## RELPS Sanctioned Providers Scraper
This project automatically scrapes the RELPS (Registro de Licitantes y Proveedores Sancionados) system from INEGI (Mexico) and exports structured sanction data to a JSON file.
The scraper is built using Playwright (sync API) for maximum stability on JavaScript-heavy ASP.NET pages and is designed to run automatically via GitHub Actions.

## 🔍 What This Scraper Does
Navigates the RELPS website
Loads the full list of sanctioned providers
Opens each provider’s detail page (ASP.NET PostBack links)

Extracts:
Provider name (proveedor)
All associated sanction case numbers (numero)
Saves the result as a structured JSON file

## ⚙️ Technology Stack
Python 3.12
Playwright (sync API)
Chromium (headless)
GitHub Actions (CI automation)


.
├── scraper.py          # Main Playwright scraper
├── relps_final.json    # Output file (auto-updated)
├── .github/
│   └── workflows/
│       └── scraper.yml # GitHub Actions workflow
└── README.md


## 🚀 How It Works
Opens the RELPS webpage
Switches into the internal iframe
Clicks "Ver total de proveedores sancionados"
Iterates through all table rows
Clicks each provider’s detail link (JavaScript PostBack)
Collects all sanction case numbers
Returns to the list and continues
Writes all data to relps_final.json


## 🤖 Automation (GitHub Actions)
The scraper runs automatically using GitHub Actions:
Daily schedule (once per day)
Manual trigger available
Commits updated relps_final.json back to the repository

# Workflow Triggers
schedule (cron)
workflow_dispatch (manual)
push to main

# Important Notes
The RELPS site uses ASP.NET JavaScript PostBack links
Direct href navigation does not work
Clicking elements is required (handled correctly in this project)
Sync Playwright was chosen over async for stability and reliability

# 📌 Why Sync Playwright?
More stable for ASP.NET + iframe-heavy websites
Easier debugging
Fewer race conditions
Works reliably in CI environments



