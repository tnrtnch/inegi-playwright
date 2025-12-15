## RELPS Sanctioned Providers Scraper<br />
This project automatically scrapes the RELPS (Registro de Licitantes y Proveedores Sancionados) system from INEGI (Mexico) and exports structured sanction data to a JSON file.<br />
The scraper is built using Playwright (sync API) for maximum stability on JavaScript-heavy ASP.NET pages and is designed to run automatically via GitHub Actions.<br />

## 🔍 What This Scraper Does<br />
Navigates the RELPS website<br />
Loads the full list of sanctioned providers<br />
Opens each provider’s detail page (ASP.NET PostBack links)<br />

Extracts:<br />
Provider name (proveedor)<br />
All associated sanction case numbers (numero)<br />
Saves the result as a structured JSON file<br />

## ⚙️ Technology Stack<br />
Python 3.12<br />
Playwright (sync API)<br />
Chromium (headless)<br />
GitHub Actions (CI automation)<br />


.<br />
├── scraper.py          # Main Playwright scraper<br />
├── relps_final.json    # Output file (auto-updated)<br />
├── .github/<br />
│   └── workflows/<br />
│       └── scraper.yml # GitHub Actions workflow<br />
└── README.md<br />


## 🚀 How It Works<br />
Opens the RELPS webpage<br />
Switches into the internal iframe<br />
Clicks "Ver total de proveedores sancionados"<br />
Iterates through all table rows<br />
Clicks each provider’s detail link (JavaScript PostBack)<br />
Collects all sanction case numbers<br />
Returns to the list and continues<br />
Writes all data to relps_final.json<br />


## 🤖 Automation (GitHub Actions)<br />
The scraper runs automatically using GitHub Actions:<br />
Daily schedule (once per day)<br />
Manual trigger available<br />
Commits updated relps_final.json back to the repository<br />

# Workflow Triggers<br />
schedule (cron)<br />
workflow_dispatch (manual)<br />
push to main<br />

# Important Notes<br />
The RELPS site uses ASP.NET JavaScript PostBack links<br />
Direct href navigation does not work<br />
Clicking elements is required (handled correctly in this project)<br />
Sync Playwright was chosen over async for stability and reliability<br />

# 📌 Why Sync Playwright?<br />
More stable for ASP.NET + iframe-heavy websites<br />
Easier debugging<br />
Fewer race conditions<br />
Works reliably in CI environments<br />




