GynoCare AI v1.0
Women's Health Intelligence Platform
Complete Setup, Usage & Troubleshooting Guide
⚠️ CRITICAL MEDICAL DISCLAIMER

THIS IS AN AI-POWERED RESEARCH AND INFORMATION TOOL ONLY.

All information is generated from published medical literature and guidelines.
Accuracy, completeness, and clinical applicability may be incomplete, outdated, or incorrect.
This is NOT a medical diagnosis, prescription, or clinical recommendation.
ALWAYS consult a qualified gynaecologist or obstetrician before:
Taking any medication
Undergoing tests, scans, or procedures
Starting fertility treatments
Making pregnancy or health-related decisions
FOR EMERGENCIES
India: 108
UK: 999
USA: 911

Do NOT rely on this platform during emergencies.

FOR RESEARCH AND EDUCATIONAL PURPOSES ONLY.

The creators accept no liability for health decisions made without professional medical consultation.

🚀 Quick Start
Windows (Recommended)
Extract the ZIP anywhere (example: C:\GynoCareAI\)
Double-click:
START_GynoCare_AI.bat
Everything installs automatically (first run: 2–5 minutes).
Browser opens automatically:
http://localhost:5055
Accept the disclaimer and begin.
First Run Notes
Internet is required during first installation.
Python packages install locally inside this folder.
Nothing is added permanently to Windows.
After setup, offline operation is possible.
Run DOWNLOAD_OFFLINE_PACKAGES.bat once to cache packages.

📁 File Structure
GynoCareAI/
├── START_GynoCare_AI.bat          ← MAIN LAUNCHER
├── DIAGNOSTIC.bat                 ← System diagnostic tool
├── REPAIR_AND_RECOVER.bat         ← Repair broken installations
├── DOWNLOAD_OFFLINE_PACKAGES.bat  ← Cache packages for offline use
├── UPDATE.bat                     ← Update dependencies
├── STOP_SERVER.bat                ← Stop the server
├── server.py                      ← Python Flask backend
├── README.md                      ← This file
├── static/
│   └── index.html                 ← Frontend application
├── uploads/                       ← Uploaded reports
├── offline_packages/              ← Cached packages
├── venv/                          ← Virtual environment
├── logs/                          ← Diagnostic and server logs
├── data/                          ← Sessions and knowledge base
└── reports_db/                    ← Generated AI reports

🔧 BAT Files Explained
File	Purpose	When To Use
START_GynoCare_AI.bat	Main launcher	Daily use
DIAGNOSTIC.bat	System health check	When problems occur
REPAIR_AND_RECOVER.bat	Fix installation issues	If startup fails
DOWNLOAD_OFFLINE_PACKAGES.bat	Cache packages offline	Run once with internet
UPDATE.bat	Update packages	Monthly
STOP_SERVER.bat	Stop server	To close GynoCare AI

💻 System Requirements
Component	Minimum	Recommended
OS	Windows 10	Windows 11
RAM	4 GB	8 GB
Storage	3 GB free	10 GB free
Internet	First setup only	Broadband
Python	Auto-installed	3.10–3.12

🤖 Platform Features

👶 Pregnancy & Maternal Care
Preconception Planning
Fertility awareness
Genetic screening
Lifestyle optimization
Folic acid supplementation
Pre-pregnancy investigations
Month-by-Month Pregnancy Guide
Baby development
Maternal changes
Nutrition advice
Scan schedules
Warning signs
Labour & Birth
Stages of labour
Pain relief options
Vaginal birth
Caesarean section
VBAC guidance
Postpartum Care
Recovery after vaginal delivery and C-section
Breastfeeding support
Postnatal mental health
Physical rehabilitation

🌸 Gynaecological Conditions

Research support for:

PCOS
Endometriosis
Fibroids
Ovarian cysts
Cervical cancer
Endometrial cancer
Adenomyosis
Vulvodynia
Ectopic pregnancy
Recurrent miscarriage
Premature ovarian insufficiency
Pre-eclampsia
Gestational diabetes mellitus (GDM)
Menstrual disorders
Menopause

…and 20+ additional conditions.

💊 Treatments & Procedures
Medical Treatments
Hormonal contraception
Ovulation induction
HRT
Obstetric medications
Surgical Procedures
Laparoscopy
Hysteroscopy
Myomectomy
LLETZ
Uterine artery embolization (UAE)

🩺 Scans & Investigations
Complete ultrasound schedule
Blood test reference ranges
Pregnancy investigations
Gynaecological diagnostic pathways

🧬 Fertility & IVF
Fertility Evaluation

Hormonal tests:

AMH
FSH
LH
Progesterone

Structural investigations:

HSG
HyCoSy
Hysteroscopy
Laparoscopy
IVF Protocols
Long protocol
Short protocol
Trigger injection
Egg collection
IVF vs ICSI
Embryo transfer
Luteal support
Success rates by age
Assisted Reproductive Technologies
IUI
Egg freezing
Donor conception
TESA / TESE
PGT-A
PGT-M
PGT-SR
Male Fertility

WHO 2021 semen analysis standards and fertility optimization.

🥗 Lifestyle & Nutrition
Diet
Fertility diet
PCOS diet
Pregnancy nutrition
Postpartum nutrition
Exercise & Yoga
Prenatal exercise
Pregnancy-safe yoga
PCOS exercise
Postpartum rehabilitation

🌷 Menopause Care

Research support for:

Perimenopause
Hormone Replacement Therapy (HRT)
Bone health
Vasomotor symptoms
Non-hormonal therapies

📚 Clinical Sources

Information references include:

ACOG — American College of Obstetricians and Gynecologists
RCOG — Royal College of Obstetricians and Gynaecologists
FOGSI — Federation of Obstetric and Gynaecological Societies of India
NICE — UK National Institute for Health and Care Excellence
ESHRE — European Society of Human Reproduction and Embryology
WHO — World Health Organization
HFEA — Human Fertilisation and Embryology Authority
PubMed — National Library of Medicine

🔑 AI Providers (5 Supported)

Without an API key, GynoCare AI operates using the embedded knowledge base.

Supported Providers
Provider	Model
OpenAI	GPT-4o
Google	Gemini 2.0 Flash
xAI	Grok 2
Anthropic	Claude Sonnet 4
DeepSeek	DeepSeek Chat

API keys are:

Stored locally in your browser.
Never sent to third-party servers.
Provider-specific and switchable.

Offline mode requires no internet.

🌐 Online vs Offline Mode
Feature	Live AI	Offline
AI Analysis	Live model	Embedded KB
Major Conditions	Full research	Core conditions
IVF Protocols	Detailed	Embedded
Upload Analysis	AI-assisted	Text extraction
Chat	AI responses	Basic responses
🇮🇳 Important Resources
Resource	Website
FOGSI India	fogsi.org
AIIMS New Delhi	aiims.edu
Apollo Fertility	apollofertility.com
Nova IVF	novaivf.com
Manipal Hospitals	manipalhospitals.com
ICMR	icmr.gov.in
CTRI India	ctri.nic.in
Women's Helpline	181
Emergency	108

🔧 Troubleshooting
BAT file closes immediately

Solution

Run:

Right-click → Run as Administrator
Browser doesn't open

Open manually:

http://localhost:5055
Python not found

The launcher downloads Python automatically.

Package installation fails

Run:

REPAIR_AND_RECOVER.bat

Choose:

Option 2 → Reinstall packages
Port already in use

Run:

STOP_SERVER.bat

Then restart GynoCare AI.

Offline mode after first setup

Run once:

DOWNLOAD_OFFLINE_PACKAGES.bat
Server errors

Inspect:

logs\server_*.log

Or run:

DIAGNOSTIC.bat

🔒 Privacy & Security
Local-first architecture.
Files remain on your computer.
No telemetry or tracking.
API keys stay inside browser local storage.
Full offline mode supported.
No third-party server dependency.

⚖️ Legal Notice

This software is provided "as is" for research and educational purposes only.

The creators make no representations regarding medical accuracy, completeness, or fitness for clinical use.

Use of this platform does not constitute a medical consultation or create a doctor-patient relationship.

The creators are not liable for health outcomes arising from use of this software.

By using this application, you acknowledge that you have read and accepted the medical disclaimer.

❤️ GynoCare AI v1.0
Women's Health Intelligence Platform

Research empowers. Your gynaecologist heals. Use both.