# GynoCare AI v1.0
## Women's Health Intelligence Platform

---

## IMPORTANT MEDICAL DISCLAIMER

**THIS IS AN AI-POWERED RESEARCH AND INFORMATION TOOL ONLY.**

- All content is AI-generated from published medical literature (ACOG, RCOG, FOGSI, WHO, NICE, ESHRE, PubMed)
- Accuracy, completeness, and clinical applicability **may be incorrect or outdated**
- This is **NOT** a medical diagnosis, prescription, or clinical recommendation
- **ALWAYS** consult a qualified gynaecologist or obstetrician before any health decision
- **FOR EMERGENCIES:** Call 108 (India) / 999 (UK) / 911 (US) — do NOT use this platform
- The creators accept **no liability** for health decisions made without professional medical consultation

---

## Quick Start (Windows)

1. Extract the ZIP to any folder (e.g., `C:\GynoCareAI\`)
2. Double-click **`START_GynoCare_AI.bat`**
3. Everything installs automatically (2-5 minutes first time)
4. Browser opens at `http://localhost:5055`
5. Accept disclaimer and begin

---

## File Structure

```
GynoCareAI/
├── START_GynoCare_AI.bat          <- MAIN LAUNCHER
├── DIAGNOSTIC.bat                 <- System health checker
├── REPAIR_AND_RECOVER.bat         <- Fix problems
├── DOWNLOAD_OFFLINE_PACKAGES.bat  <- Save packages for offline
├── UPDATE.bat                     <- Update to latest versions
├── STOP_SERVER.bat                <- Stop the server
├── server.py                      <- Python Flask backend
├── README.md                      <- This file
├── static/
│   └── index.html                 <- Full web application
├── uploads/                       <- Your uploaded reports
├── offline_packages/              <- Cached Python packages
├── venv/                          <- Python environment (auto-created)
├── logs/                          <- Server and diagnostic logs
├── data/                          <- Knowledge base and sessions
└── reports_db/                    <- Generated AI reports
```

---

## What's Covered

### Pregnancy
- **Pre-Pregnancy Planning** — Preconception tests, fertility awareness, lifestyle optimisation, folic acid, genetic screening
- **Month-by-Month Pregnancy Guide** — All 9 months with baby development, maternal changes, scan schedule, nutrition, warning signs
- **Labour & Birth** — Stages of labour, types of delivery, pain relief options, VBAC
- **Post-Pregnancy Care** — Physical recovery (vaginal and CS), breastfeeding, postnatal mental health, physical rehabilitation

### Gynaecology
- **Conditions** — PCOS, Endometriosis, Fibroids, Ovarian Cysts, Cervical Cancer, Endometrial Cancer, Pre-eclampsia, GDM, Ectopic Pregnancy, Recurrent Miscarriage, Adenomyosis, Vulvodynia, Premature Ovarian Insufficiency, and 20+ more
- **Treatments** — Hormonal contraception, ovulation induction agents, surgical procedures (laparoscopy, hysteroscopy, LLETZ, myomectomy, UAE), key obstetric medicines
- **Scans & Tests** — Complete obstetric ultrasound schedule, blood test reference ranges, gynaecological investigation guide

### Fertility & IVF
- **Fertility Evaluation** — Hormonal tests (FSH, LH, AMH, progesterone), structural investigations (HyCoSy, HSG, hysteroscopy, laparoscopy)
- **IVF Protocol** — Long and short protocols, trigger, egg collection, fertilisation (IVF vs ICSI), embryo transfer, luteal support, success rates by age
- **ART** — IUI, egg freezing, donor conception, surgical sperm retrieval (TESA/TESE), PGT-A/M/SR
- **Male Fertility** — WHO 2021 semen analysis parameters, improvement strategies

### Lifestyle
- **Diet & Nutrition** — Trimester-specific nutrition, fertility diet, PCOS diet, postpartum nutrition
- **Exercise & Yoga** — Safe exercise in pregnancy, prenatal yoga sequence, return-to-exercise timeline, PCOS exercise
- **Menopause** — Perimenopause, HRT types and routes, bone health, non-hormonal options

---

## Clinical Sources

All information referenced from:
- **ACOG** — American College of Obstetricians and Gynecologists
- **RCOG** — Royal College of Obstetricians and Gynaecologists (UK)
- **FOGSI** — Federation of Obstetric and Gynaecological Societies of India
- **NICE** — National Institute for Health and Care Excellence (UK)
- **ESHRE** — European Society of Human Reproduction and Embryology
- **WHO** — World Health Organization
- **HFEA** — Human Fertilisation and Embryology Authority (IVF data)
- **PubMed** — National Library of Medicine research database

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10 | Windows 11 |
| RAM | 4 GB | 8 GB |
| Storage | 3 GB free | 10 GB free |
| Internet | For first setup | For live AI |
| Python | Auto-installed | 3.10-3.12 |

---

## Choose Your AI Provider (5 Options)

Without any API key, the platform works in **offline research mode** using the embedded clinical knowledge base.

To enable live AI analysis, go to **Settings** in the sidebar and pick ONE of 5 supported AI providers — each with its own free or paid API key:

| Provider | Model Used | Get a Free Key |
|----------|-----------|-----------------|
| **Claude** (Anthropic) | claude-sonnet-4 | console.anthropic.com |
| **ChatGPT** (OpenAI) | gpt-4o | platform.openai.com/api-keys |
| **Gemini** (Google) | gemini-2.0-flash | aistudio.google.com/apikey |
| **Grok** (xAI) | grok-2-latest | console.x.ai |
| **DeepSeek** | deepseek-chat | platform.deepseek.com/api_keys |

Click a provider card, paste its key, and click Save. Your key is stored **only in your browser's local storage** — it is sent directly to that provider's API and never touches any third-party server. You can switch providers at any time; each provider's key is remembered separately so you don't have to re-enter it.

If you don't add any key, simply select **Offline Mode** — the platform will use its built-in women's health knowledge base with zero internet dependency.

---

## Online vs Offline Mode

| Feature | Live AI (API key + internet) | Offline Mode |
|---------|------------------------------|--------------|
| Analysis | Live Claude AI | Embedded knowledge base |
| Conditions | Full clinical research | Major conditions covered |
| IVF protocols | Detailed, current | Core protocols embedded |
| Report upload | Text extraction + AI | Text extraction only |
| Chat | AI-powered responses | Basic keyword responses |

---

## India-Specific Resources

| Resource | Contact |
|----------|---------|
| FOGSI India | fogsi.org |
| AIIMS, New Delhi | aiims.edu |
| Apollo Fertility | apollofertility.com |
| Nova IVF | novaivf.com |
| Manipal Hospitals | manipalhospitals.com |
| ICMR | icmr.gov.in |
| CTRI India (clinical trials) | ctri.nic.in |
| Emergency | 108 |
| Women's helpline | 181 |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Double-click does nothing | Right-click → Run as Administrator |
| Python not found | Launcher downloads it automatically (needs internet) |
| Browser doesn't open | Go to http://localhost:5055 manually |
| Port in use | Run STOP_SERVER.bat, then START again |
| Package install fails | Run REPAIR_AND_RECOVER.bat → Option 2 |
| Works offline after first run | Run DOWNLOAD_OFFLINE_PACKAGES.bat once |
| Server starts but errors | Check logs\server_*.log |

---

## Legal Notice

This software is provided for research and educational purposes only. The creators make no representations about medical accuracy, completeness, or fitness for clinical use. Use of this tool does not constitute a medical consultation or professional relationship. The creators are not liable for any health outcomes arising from use of this platform. By using this software you confirm you have read and accepted the full medical disclaimer.

---

*GynoCare AI v1.0 — Women's Health Intelligence Platform*
*Research empowers. Your gynaecologist heals. Use both.*
