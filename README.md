# GynoCare AI v1.0
## Women's Health Intelligence Platform
### Complete Setup, Usage & Troubleshooting Guide

---

## ⚠️ CRITICAL MEDICAL DISCLAIMER

**THIS IS AN AI-POWERED RESEARCH AND INFORMATION TOOL ONLY.**

- All information is generated from published medical literature and guidelines.
- Accuracy, completeness, and clinical applicability **may be incomplete, outdated, or incorrect**.
- This is **NOT** a medical diagnosis, prescription, or clinical recommendation.
- **ALWAYS** consult a qualified gynaecologist or obstetrician before:
  - Taking any medication
  - Undergoing tests, scans, or procedures
  - Starting fertility treatments
  - Making pregnancy or health-related decisions.

### 🚑 Emergency Numbers

| Country | Number |
|----------|---------|
| India | 108 |
| UK | 999 |
| USA | 911 |

**FOR RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

The creators accept **no liability** for health decisions made without professional medical consultation.

---

## 🚀 Quick Start

### Windows (Recommended)

1. Extract the ZIP anywhere (example: `C:\GynoCareAI\`)
2. Double-click **`START_GynoCare_AI.bat`**
3. Everything installs automatically (first run: 2–5 minutes)
4. Browser opens automatically:

```text
http://localhost:5055
```

5. Accept the disclaimer and begin.

### First Run Notes

- Internet is required during first installation.
- Python packages install locally inside this folder.
- Nothing is added permanently to Windows.
- After setup, offline operation is possible.
- Run **`DOWNLOAD_OFFLINE_PACKAGES.bat`** once to cache packages.

---

## 📁 File Structure

```text
GynoCareAI/
├── START_GynoCare_AI.bat          ← MAIN LAUNCHER
├── DIAGNOSTIC.bat                 ← System diagnostic tool
├── REPAIR_AND_RECOVER.bat         ← Repair broken installations
├── DOWNLOAD_OFFLINE_PACKAGES.bat  ← Cache packages for offline use
├── UPDATE.bat                     ← Update dependencies
├── STOP_SERVER.bat                ← Stop the server
├── server.py                      ← Python Flask backend
├── README.md                      ← This file
│
├── static/
│   └── index.html                 ← Frontend application
│
├── uploads/                       ← Uploaded reports
├── offline_packages/              ← Cached packages
├── venv/                          ← Virtual environment
├── logs/                          ← Diagnostic and server logs
├── data/                          ← Sessions and knowledge base
└── reports_db/                    ← Generated AI reports
```

---

## 🔧 BAT Files Explained

| File | Purpose | When To Use |
|--------|---------|-------------|
| `START_GynoCare_AI.bat` | Main launcher | Daily use |
| `DIAGNOSTIC.bat` | System health check | When problems occur |
| `REPAIR_AND_RECOVER.bat` | Fix installation issues | If startup fails |
| `DOWNLOAD_OFFLINE_PACKAGES.bat` | Cache packages offline | Run once with internet |
| `UPDATE.bat` | Update packages | Monthly |
| `STOP_SERVER.bat` | Stop server | To close GynoCare AI |

---

## 💻 System Requirements

| Component | Minimum | Recommended |
|------------|---------|-------------|
| OS | Windows 10 | Windows 11 |
| RAM | 4 GB | 8 GB |
| Storage | 3 GB free | 10 GB free |
| Internet | First setup only | Broadband |
| Python | Auto-installed | 3.10–3.12 |

---

## 🤖 Platform Features

### 👶 Pregnancy & Maternal Care

#### Preconception Planning

- Fertility awareness
- Genetic screening
- Lifestyle optimization
- Folic acid supplementation
- Pre-pregnancy investigations

#### Month-by-Month Pregnancy Guide

- Baby development
- Maternal changes
- Nutrition advice
- Scan schedules
- Warning signs

...
