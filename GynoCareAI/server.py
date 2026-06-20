"""
GynoCare AI — Production Backend Server v1.0
Women's Health Intelligence Platform
=============================================
DISCLAIMER: All AI output is for research/education only.
Not medical advice. Always consult a qualified gynaecologist.
"""

import os
import sys
import json
import uuid
import logging
import datetime
import argparse
from pathlib import Path

try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
    FLASK_OK = True
except ImportError:
    print("[FATAL] Flask not installed. Run REPAIR_AND_RECOVER.bat")
    sys.exit(1)

try:
    import requests as req_lib
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import fitz
    FITZ_OK = True
except ImportError:
    FITZ_OK = False

# ── Multi-provider AI module ─────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent / "modules"))
try:
    import ai_providers
    AI_PROVIDERS_OK = True
except ImportError:
    AI_PROVIDERS_OK = False

# ── Configuration ────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.resolve()
UPLOAD_DIR  = BASE_DIR / "uploads"
LOGS_DIR    = BASE_DIR / "logs"
DATA_DIR    = BASE_DIR / "data"
STATIC_DIR  = BASE_DIR / "static"
REPORTS_DIR = BASE_DIR / "reports_db"

for d in [UPLOAD_DIR, LOGS_DIR, DATA_DIR, STATIC_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PORT    = int(os.environ.get("GYNOCARE_PORT", 5055))
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")  # legacy/back-compat default
# Server-side default keys per provider (optional; client can also send its own key per-request)
DEFAULT_PROVIDER_KEYS = ai_providers.get_env_keys() if AI_PROVIDERS_OK else {}
VERSION = "1.0.0"

DISCLAIMER = (
    "⚠️ AI RESEARCH DISCLAIMER: All output is AI-generated from published medical "
    "literature (ACOG, RCOG, FOGSI, WHO, PubMed). This is for educational research only. "
    "NOT a medical diagnosis or prescription. ALWAYS consult a qualified gynaecologist "
    "or obstetrician before any health decision. For emergencies call 108/999/911 immediately."
)

# ── Logging ──────────────────────────────────────────────────────
log_file = LOGS_DIR / f"server_{datetime.date.today()}.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("GynoCareAI")

# ── Flask App ────────────────────────────────────────────────────
app = Flask(__name__, static_folder=str(STATIC_DIR))
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024
CORS(app, origins="*")

# ══════════════════════════════════════════════════════════════════
# OFFLINE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════
KNOWLEDGE = {
    "pcos": {
        "name": "PCOS (Polycystic Ovary Syndrome)",
        "prevalence": "8-13% of reproductive-age women worldwide. Most common hormonal disorder in women.",
        "diagnosis": "Rotterdam Criteria (2 of 3): Oligomenorrhoea/amenorrhoea, clinical/biochemical hyperandrogenism, polycystic ovarian morphology on USG (≥20 follicles 2-9mm per ovary OR ovarian volume >10mL).",
        "investigations": ["FSH, LH (Day 2-3) — LH:FSH ratio >2:1 suggests PCOS", "Total testosterone, DHEAS, SHBG, free androgen index", "AMH — often elevated >3.5 ng/mL", "Fasting glucose, fasting insulin, OGTT, HbA1c", "TSH, Prolactin — exclude other causes", "Transvaginal ultrasound"],
        "treatment": {
            "lifestyle": "5-10% weight loss in overweight PCOS restores ovulation in 80%. Low GI diet, exercise 150+ min/week.",
            "menstrual_regulation": "COCP (combined oral contraceptive pill) with anti-androgen progestogen (cyproterone acetate/drospirenone). Cyclical progestins every 3 months minimum to prevent endometrial hyperplasia.",
            "insulin_sensitisation": "Metformin 500-1000mg twice daily. Myo-Inositol 2g + D-chiro-inositol 50mg twice daily (strong evidence, well-tolerated).",
            "ovulation_induction": "Letrozole 2.5-7.5mg Day 2-6 (first-line per ESHRE 2023). Clomiphene citrate 50-150mg (second-line). Gonadotrophins with close monitoring. Laparoscopic ovarian drilling for clomiphene-resistant PCOS.",
            "hirsutism": "Spironolactone 50-200mg/day, Finasteride 5mg/day, COCP with cyproterone, laser hair removal."
        },
        "long_term_risks": ["Type 2 Diabetes: 5-7x higher risk — screen every 1-3 years with OGTT", "Endometrial cancer: 3x higher risk — ensure regular withdrawal bleeds", "Cardiovascular disease, hypertension, dyslipidaemia", "Obstructive sleep apnoea (screen in obese PCOS)", "Depression, anxiety, eating disorders (50%+ have psychological comorbidity)"],
        "supplements_evidence": ["Myo-Inositol 2g + D-chiro-inositol 50mg BD — strongest evidence for insulin resistance and ovulation", "Vitamin D — commonly deficient, supplementation improves insulin sensitivity", "CoQ10 600mg/day — improves oocyte quality", "Spearmint tea 2 cups/day — reduces free testosterone (RCT evidence)", "NAC (N-acetyl cysteine) — antioxidant, improves insulin sensitivity"],
        "diet_specifics": ["Low GI carbohydrates: oats, legumes, bajra, jowar, quinoa, brown rice", "Anti-inflammatory: turmeric, ginger, berries, olive oil, fatty fish", "Protein at every meal: reduces glycaemic impact", "Fibre 25-30g/day: psyllium husk, vegetables, legumes", "Avoid: refined carbs, sugar, processed foods, alcohol", "Cinnamon 1/2 tsp/day: improves insulin sensitivity (small RCT evidence)"]
    },
    "endometriosis": {
        "name": "Endometriosis",
        "prevalence": "10-15% of reproductive-age women. 30-40% of women with infertility. Average diagnostic delay: 7-12 years.",
        "sites": "Peritoneum, ovaries (endometrioma), fallopian tubes, Pouch of Douglas, rectovaginal septum, bladder, bowel (rare: diaphragm, pleura, distant sites).",
        "staging": "ASRM classification I-IV (minimal, mild, moderate, severe) based on laparoscopic findings. Stage does not correlate with pain severity.",
        "symptoms": ["Dysmenorrhoea — worsening over years, often severe, not adequately relieved by standard analgesia", "Deep dyspareunia — pain during or after intercourse", "Chronic pelvic pain — cyclical and non-cyclical", "Dyschezia — painful defaecation especially during menstruation", "Dysuria — painful urination during menstruation", "Subfertility/infertility", "Fatigue, bloating (especially premenstrual)"],
        "diagnosis": "Laparoscopy + biopsy is the only definitive diagnosis. Clinical suspicion from symptoms. TVUS for endometriomas and Pouch of Douglas assessment. MRI for deep infiltrating endometriosis (DIE). CA-125 elevated in severe disease but non-specific.",
        "treatment": {
            "medical": "COCP (continuous reduces menstruation frequency). Progestogens: Norethisterone 5mg BD, Medroxyprogesterone acetate, Mirena IUS (excellent for pain). GnRH analogues (create temporary menopause — 6 months max without add-back). Dienogest 2mg/day (licensed specifically for endometriosis). Elagolix (GnRH antagonist — oral, flexible dosing).",
            "surgical": "Laparoscopic excision of endometriosis (gold standard — removes implants rather than ablating). Ovarian cystectomy for endometrioma >4cm. Radical surgery for DIE. Hysterectomy ± BSO only for completed family with severe disease.",
            "fertility": "IVF most effective for endometriosis-associated infertility (especially stages III-IV). Surgical treatment of Stage I-II improves spontaneous conception rates. Medical suppression before IVF (3-6 months GnRH analogue — 'long protocol') improves outcomes in severe endometriosis.",
            "pain": "NSAIDs first-line for dysmenorrhoea. Multidisciplinary pain management for chronic pain. Physiotherapy (pelvic floor rehabilitation). CBT for chronic pain. TENS device."
        }
    },
    "fibroids": {
        "name": "Uterine Fibroids (Leiomyoma)",
        "prevalence": "20-40% of women over 35. Most common benign uterine tumour. More prevalent and symptomatic in women of African descent.",
        "types": "Submucosal (inside cavity — most symptomatic: heavy bleeding, infertility), Intramural (within myometrium), Subserosal (outer surface), Pedunculated (on stalk), Cervical (rare).",
        "symptoms": ["Heavy menstrual bleeding (HMB) — most common symptom of submucosal fibroids", "Pelvic pressure, bulk symptoms", "Urinary frequency/urgency (large fibroids compressing bladder)", "Constipation (posterior fibroids)", "Subfertility (submucosal > intramural > subserosal)", "Dysmenorrhoea", "Back pain"],
        "investigations": ["Transvaginal ultrasound: First-line. Identifies number, size, location, vascularity (FIGO classification)", "MRI: Superior for mapping multiple fibroids pre-myomectomy, adenomyosis differentiation", "Saline Infusion Sonography (SIS): Better defines submucosal component", "Hysteroscopy: Gold standard for submucosal fibroids", "Blood tests: FBC (anaemia from HMB), TSH"],
        "treatment": {
            "medical": "Tranexamic acid 1g TDS (reduce bleeding 50%). NSAIDs (reduce bleeding + pain). Mirena IUS (reduces bleeding 90% — first-line medical for HMB with intramural fibroids). COCP. GnRH analogues (shrink fibroid 30-50% — use as pre-surgical treatment max 6 months). Ulipristal acetate (temporarily suspended in some countries due to liver concerns). Relugolix (oral GnRH antagonist — licensed for fibroids in some countries).",
            "surgical": "Hysteroscopic myomectomy: Submucosal fibroids. Day case, outpatient. Laparoscopic myomectomy: Subserosal/intramural ≤8-10cm. Faster recovery. Open myomectomy (laparotomy): Large/multiple fibroids. UAE (Uterine Artery Embolisation): Radiological. All fibroid types. Fibroids shrink 50%. Outpatient. Fertility outcomes less certain. Hysterectomy: Definitive treatment — only for completed family.",
            "non_surgical": "Focused Ultrasound Surgery (MRgFUS): Non-invasive, MRI-guided. Fibroids heated and destroyed. Limited availability."
        }
    },
    "preeclampsia": {
        "name": "Pre-eclampsia",
        "definition": "Hypertension (BP ≥140/90 on two occasions ≥4 hours apart) + proteinuria (PCR ≥30mg/mmol or ≥300mg/24hrs) OR severe features — after 20 weeks gestation.",
        "incidence": "3-5% of pregnancies. Leading cause of maternal and perinatal mortality worldwide.",
        "risk_factors": ["First pregnancy (most important risk factor)", "Previous pre-eclampsia", "Multiple pregnancy (twins/triplets)", "BMI >35", "Diabetes, hypertension, kidney disease, autoimmune conditions", "Age >40 or <18", "Family history", "Interpregnancy interval >10 years", "ART/IVF conception"],
        "prevention": "Aspirin 150mg/day from 12 weeks to 36 weeks for high-risk women (reduces risk by 62% per ASPRE trial). Calcium supplementation 1.5-2g/day in low calcium intake populations.",
        "management": {
            "mild": "Outpatient monitoring if BP controlled and no severe features. Antihypertensives: Labetalol (first-line), Nifedipine (second-line), Methyldopa (well-established safety). Target BP <135/85. Twice-weekly CTG, weekly growth scans. Deliver at 37 weeks.",
            "severe": "Admit to hospital. IV Labetalol/Hydralazine for acute hypertension (BP ≥160/110). IV Magnesium Sulphate (MgSO4) for seizure prophylaxis and treatment of eclampsia. Foetal monitoring. Delivery — only cure. Timing depends on gestational age and severity.",
            "hellp": "HELLP syndrome: Haemolysis + Elevated Liver enzymes + Low Platelets. Obstetric emergency. Immediate delivery regardless of gestational age."
        },
        "postpartum": "BP can worsen in first 5 days postpartum. Continue antihypertensives. Long-term: 4x lifetime risk of hypertension, 2x risk of cardiovascular disease, stroke, kidney disease. Annual BP and metabolic monitoring for life."
    },
    "ivf": {
        "name": "IVF (In Vitro Fertilisation)",
        "success_rates": {"under_35": "35-40% live birth per cycle", "35_37": "25-30%", "38_39": "18-22%", "40_42": "10-15%", "43_44": "5-7%", "over_44": "2-3% own eggs; significantly higher with donor eggs"},
        "protocol_long": ["Day 21 previous cycle: GnRH agonist (Buserelin/Lupron) for down-regulation", "Day 2-3: Baseline scan confirms down-regulation. Start FSH stimulation (Gonal-F, Menopur, Fostimon)", "Days 3-13: Daily injections. Monitoring scans every 2-3 days. Target: 3+ follicles ≥17mm", "Trigger: hCG (Ovitrelle) or GnRH agonist when follicles ready", "Egg Collection (OPU): Transvaginal aspiration under sedation, 36 hours after trigger", "Fertilisation: Conventional IVF or ICSI (single sperm injected into egg)", "Embryo development: Monitored Day 1-6. Blastocyst transfer Day 5-6 preferred", "Transfer: Fresh (Day 3 or 5) or frozen embryo transfer (FET) in subsequent cycle", "Luteal support: Progesterone pessaries/injections until 12 weeks if pregnant", "Beta-hCG: 14 days after transfer"],
        "ohss": "OHSS (Ovarian Hyperstimulation Syndrome): 1-2% severe. Risk: PCOS, young women, high AFC, AMH >3.5. Prevention: GnRH antagonist protocol, freeze-all strategy, lower gonadotrophin doses, GnRH agonist trigger.",
        "pgt": "Preimplantation Genetic Testing: PGT-A (aneuploidies — improves implantation rate, reduces miscarriage), PGT-M (specific genetic conditions — Thalassaemia, BRCA), PGT-SR (structural rearrangements in parents)."
    },
    "pregnancy_nutrition": {
        "trimester_1": {"extra_calories": "+0-100 kcal/day", "key_nutrients": ["Folic acid 400mcg/day (supplement) + leafy greens, lentils, fortified cereals", "Iron: Spinach+Vit C, dal, jaggery, pomegranate, ragi", "Vitamin B6 25mg TDS for nausea", "Iodine 150mcg/day"], "avoid": ["Alcohol — completely", "Raw/undercooked meat and eggs", "Unpasteurised milk and soft cheeses", "Raw papaya and pineapple", "Excess Vitamin A (liver)", "Caffeine >200mg/day", "High-mercury fish: shark, swordfish, king mackerel"]},
        "trimester_2": {"extra_calories": "+300 kcal/day", "key_nutrients": ["Calcium 1000mg/day: milk, curd, paneer, ragi, sesame, almonds", "DHA omega-3: fatty fish or algae supplement (vegetarians)", "Protein 1.1-1.3g/kg/day: dal, rajma, eggs, paneer, chicken", "Iron continues: haemoglobin monitored every 4 weeks"]},
        "trimester_3": {"extra_calories": "+450 kcal/day", "key_nutrients": ["All second trimester nutrients continue", "Vitamin K: leafy greens", "GDM diet if diagnosed: low GI, portion-controlled carbs, increase protein/fat"], "common_issues": ["Heartburn: small frequent meals, avoid lying down after eating, elevate head of bed", "Constipation: 2.5-3L water, high fibre, gentle movement", "Oedema: reduce salt, elevate legs, stay active — if sudden onset with headache, check BP"]}
    },
    "menopause": {
        "name": "Menopause",
        "definition": "12 consecutive months without menstruation. Average age 51 UK/US; 47.5 years India. Premature Ovarian Insufficiency (POI) = before 40.",
        "symptoms": ["Vasomotor: Hot flushes (73%), night sweats, palpitations", "Genitourinary Syndrome (GSM): Vaginal dryness, dyspareunia, urinary urgency/frequency, recurrent UTIs", "Psychological: Mood changes, anxiety, depression, brain fog, poor concentration", "Sleep disturbance — often secondary to night sweats", "Musculoskeletal: Joint pains, muscle aches", "Accelerated bone loss — osteoporosis risk", "Skin and hair thinning"],
        "hrt": {
            "types": "Combined (oestrogen + progestogen) for intact uterus. Oestrogen-only post-hysterectomy. Sequential (monthly bleed) or continuous (no bleed after 1 year).",
            "routes": "Transdermal (patch, gel, spray) — lower VTE and stroke risk than oral. Oral — convenient. Vaginal (local for GSM — minimal systemic absorption).",
            "bioidentical": "Body-identical: Oestradiol + micronised progesterone (Utrogestan/Prometrium) — best regulated safety evidence.",
            "benefits": ["Most effective for vasomotor symptoms and GSM", "Prevents osteoporosis — reduces fracture risk 30-40%", "Reduces all-cause mortality when started before 60 (WHI re-analysis 2022)", "Cardioprotective within 10 years of menopause", "Reduces T2DM, colorectal cancer risk"],
            "risks": "Small increased breast cancer risk with combined HRT (after 5+ years). Transdermal oestrogen does not increase VTE. Individual benefit-risk assessment essential.",
            "non_hormonal": "Fezolinetant (Veozah — non-hormonal, non-SSRI, FDA 2023). SSRIs/SNRIs (venlafaxine, escitalopram). Gabapentin. Vaginal oestrogen (safe even for breast cancer survivors per BMS 2023)."
        },
        "bone_health": "DEXA scan: T-score normal ≥-1.0; Osteopaenia -1.0 to -2.5; Osteoporosis ≤-2.5. Calcium 1200mg/day + Vitamin D 1000-2000 IU/day. Weight-bearing exercise + resistance training. Bisphosphonates if osteoporosis confirmed."
    },
    "fertility_diet": {
        "evidence_base": "Mediterranean Diet pattern has strongest evidence for fertility improvement (Human Reproduction 2019 meta-analysis).",
        "beneficial": ["CoQ10 600mg/day — improves egg quality and sperm parameters (multiple RCTs)", "Myo-Inositol 2g + D-chiro-inositol 50mg BD — PCOS ovulation restoration", "Omega-3 DHA/EPA — improved endometrial receptivity and egg quality", "Antioxidants (Vit C, Vit E, selenium) — reduce oxidative stress on eggs and sperm", "Full-fat dairy 1 portion/day — Nurses' Health Study: lower ovulatory infertility risk", "Plant protein preferred over animal protein for ovulatory fertility (Chavarro NEJM 2007)"],
        "avoid": ["Trans fats — 2% increase in trans fat calories = 73% increase in ovulatory infertility", "Alcohol >2 units/day — reduces IVF success 13-24%", "High-mercury fish — accumulates in oocytes", "High GI foods — worsen insulin resistance, impair PCOS ovulation"],
        "male_fertility": ["CoQ10 200-600mg/day — improves sperm motility and morphology", "Lycopene 6mg/day — improves sperm concentration", "Zinc 66mg/day — testosterone production, sperm morphology", "Selenium 100-200mcg/day — sperm motility", "Vitamin D — testosterone production", "Avoid: anabolic steroids, marijuana, scrotal heat (tight underwear, laptop on lap, >40°C baths)"]
    }
}

def save_knowledge():
    with open(DATA_DIR / "gyno_knowledge.json", "w", encoding="utf-8") as f:
        json.dump(KNOWLEDGE, f, indent=2, ensure_ascii=False)

def load_sessions():
    sf = DATA_DIR / "sessions.json"
    if sf.exists():
        with open(sf, "r") as f:
            return json.load(f)
    return {}

def save_session(sid, data):
    sessions = load_sessions()
    sessions[sid] = {**data, "updated": datetime.datetime.now().isoformat()}
    with open(DATA_DIR / "sessions.json", "w") as f:
        json.dump(sessions, f, indent=2)

def is_online():
    if not REQUESTS_OK:
        return False
    try:
        req_lib.get("https://8.8.8.8", timeout=3)
        return True
    except:
        return False

def extract_pdf_text(filepath):
    if not FITZ_OK:
        return "[PDF extraction unavailable — PyMuPDF not installed]"
    try:
        doc = fitz.open(str(filepath))
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text[:8000]
    except Exception as e:
        return f"[PDF extraction error: {e}]"

DEFAULT_SYSTEM_PROMPT = (
    "You are GynoCare AI, a women's health research assistant. You help patients understand "
    "gynaecological and obstetric information from published medical literature. "
    "ALWAYS begin with a brief disclaimer that this is AI research. "
    "Provide thorough, compassionate, evidence-based information. "
    "Reference ACOG, RCOG, FOGSI, and WHO guidelines where relevant. "
    "ALWAYS end with a reminder to consult a qualified gynaecologist or obstetrician. "
    "Be specific with clinical details. Never refuse to provide educational information."
)

def call_claude(prompt, system_prompt=None, max_tokens=2500, provider=None, api_key=None):
    """
    Multi-provider AI call. Defaults to 'anthropic' with the server's ANTHROPIC_API_KEY
    for backward compatibility, but accepts provider= and api_key= to route to any
    of the 5 supported providers (anthropic, openai, gemini, grok, deepseek).
    """
    if not AI_PROVIDERS_OK:
        return None, "ai_providers_module_missing"

    provider = (provider or "anthropic").lower()
    if provider not in ai_providers.PROVIDERS:
        provider = "anthropic"

    effective_key = api_key or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider == "anthropic" else "")

    if not effective_key or not REQUESTS_OK or not is_online():
        return None, "offline_or_no_key"

    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    text, mode = ai_providers.call_ai(provider, effective_key, prompt, system_prompt, max_tokens)
    if text is None:
        log.error(f"{provider} API error: {mode}")
        return None, mode
    return text, "live_ai"

def build_offline_response(topic, details="", patient_info=None):
    """Build comprehensive offline response from knowledge base."""
    topic_l = topic.lower()
    kb_key = None
    for key in KNOWLEDGE:
        if key in topic_l or topic_l in key or topic_l in KNOWLEDGE[key].get("name","").lower():
            kb_key = key
            break

    lines = [
        f"# GynoCare AI Research Report",
        f"**Topic:** {topic}",
        f"**Mode:** Offline Research (Embedded Clinical Knowledge Base)",
        f"",
        f"> ⚠️ **DISCLAIMER:** This is AI-generated educational information from published medical literature "
        f"(ACOG, RCOG, FOGSI, WHO). NOT a medical diagnosis or prescription. "
        f"ALWAYS consult a qualified gynaecologist/obstetrician before any decision.",
        f"",
        f"---",
        f""
    ]

    if kb_key:
        kb = KNOWLEDGE[kb_key]
        name = kb.get("name", topic)
        lines.append(f"## {name}")
        lines.append("")

        for field, value in kb.items():
            if field == "name":
                continue
            if isinstance(value, str):
                lines.append(f"**{field.replace('_',' ').title()}:** {value}")
                lines.append("")
            elif isinstance(value, list):
                lines.append(f"### {field.replace('_',' ').title()}")
                for item in value:
                    lines.append(f"- {item}")
                lines.append("")
            elif isinstance(value, dict):
                lines.append(f"### {field.replace('_',' ').title()}")
                for sub_key, sub_val in value.items():
                    if isinstance(sub_val, str):
                        lines.append(f"**{sub_key.replace('_',' ').title()}:** {sub_val}")
                    elif isinstance(sub_val, list):
                        lines.append(f"**{sub_key.replace('_',' ').title()}:**")
                        for item in sub_val:
                            lines.append(f"  - {item}")
                    lines.append("")
    else:
        lines += [
            f"## Research Overview: {topic}",
            "",
            f"Based on the embedded clinical knowledge base, here is research-based information about {topic}:",
            "",
            "**Clinical Guideline Sources:** ACOG (American College of Obstetricians and Gynecologists), "
            "RCOG (Royal College of Obstetricians and Gynaecologists), FOGSI (Federation of Obstetric and "
            "Gynaecological Societies of India), WHO (World Health Organization), NICE (UK), ESHRE (Europe).",
            "",
            "For detailed information on this specific topic, please enable live AI by adding your "
            "Anthropic API key in Settings, or consult a qualified gynaecologist directly.",
            ""
        ]

    lines += [
        "---",
        "",
        "## India Clinical Resources",
        "",
        "- **FOGSI India:** fogsi.org — National gynaecology guidelines",
        "- **ICMR:** icmr.gov.in — Indian clinical research",
        "- **CTRI India:** ctri.nic.in — Clinical trials registry",
        "- **Apollo Hospitals Fertility:** apollofertility.com",
        "- **Nova IVF:** novaivf.com",
        "- **Manipal Hospitals:** manipalhospitals.com",
        "- **AIIMS, New Delhi:** aiims.edu",
        "",
        "---",
        "",
        f"⚠️ **{DISCLAIMER}**"
    ]

    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return send_from_directory(str(STATIC_DIR), "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(str(STATIC_DIR), filename)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok", "version": VERSION,
        "online": is_online(), "api_key_set": bool(API_KEY),
        "live_ai": bool(API_KEY and is_online()),
        "pdf_extract": FITZ_OK, "image_process": PIL_OK,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/api/upload", methods=["POST"])
def upload():
    if "files" not in request.files:
        return jsonify({"error": "No files"}), 400
    session_id = request.form.get("session_id") or str(uuid.uuid4())
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for f in request.files.getlist("files"):
        if not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        safe = f"{uuid.uuid4().hex}{ext}"
        dest = session_dir / safe
        f.save(str(dest))
        extracted = ""
        ftype = "unknown"
        if ext == ".pdf":
            extracted = extract_pdf_text(dest)
            ftype = "pdf"
        elif ext in [".jpg",".jpeg",".png",".bmp",".dcm"]:
            ftype = "image"
        elif ext in [".txt",".csv"]:
            try: extracted = dest.read_text(encoding="utf-8", errors="ignore")[:5000]
            except: pass
            ftype = "text"
        results.append({"original": f.filename, "saved": safe, "type": ftype,
                        "size_kb": round(dest.stat().st_size/1024,1), "has_content": bool(extracted)})
    existing = load_sessions().get(session_id, {})
    existing_files = existing.get("files", []) + results
    save_session(session_id, {"session_id": session_id, "files": existing_files})
    return jsonify({"success": True, "session_id": session_id, "uploaded": len(results), "files": results, "disclaimer": DISCLAIMER})

@app.route("/api/analyse", methods=["POST"])
def analyse():
    data = request.json or {}
    topic        = data.get("topic", "General Gynaecology")
    condition    = data.get("condition", "")
    stage        = data.get("stage", "")
    patient_info = data.get("patient_info", {})
    section      = data.get("section", "general")
    session_id   = data.get("session_id", "")
    api_key_from_client = data.get("api_key", "")
    provider     = data.get("provider", "anthropic")
    effective_key = api_key_from_client or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider=="anthropic" else "")

    log.info(f"Analysis: topic={topic} section={section} provider={provider}")

    file_context = ""
    if session_id:
        sessions = load_sessions()
        if session_id in sessions:
            files = sessions[session_id].get("files", [])
            if files:
                file_context = f"\n\nUploaded Reports ({len(files)} files):\n"
                for fi in files[:10]:
                    file_context += f"- {fi['original']} ({fi['type']}, {fi['size_kb']} KB)\n"

    prompt = f"""
Women's Health Research Request:
Topic/Condition: {topic}
Specific Condition: {condition}
Patient Age: {patient_info.get('age','Not specified')}
Cycle History: {patient_info.get('cycle','Not specified')}
Symptoms: {patient_info.get('symptoms','Not specified')}
Current Treatment: {patient_info.get('treatment','None specified')}
Other Conditions: {patient_info.get('conditions','None')}
Section Requested: {section}
{file_context}

Please provide comprehensive research covering:
1. Overview and clinical context
2. Diagnosis criteria and investigations (with specific tests and normal ranges)
3. Evidence-based treatment options (medical and surgical)
4. Relevant medications with dosing information from clinical guidelines
5. Diet and lifestyle recommendations
6. When to seek emergency care
7. India-specific resources, hospitals, and guidelines (FOGSI)
8. Questions to ask their gynaecologist
9. Recent developments and clinical trial information

Reference ACOG, RCOG, FOGSI, NICE guidelines. Be specific and compassionate.
"""
    result, mode = call_claude(prompt, provider=provider, api_key=effective_key) if (effective_key and is_online()) else (None, "offline")
    if not result:
        result = build_offline_response(topic, condition, patient_info)
        mode = "offline"
    return jsonify({"success": True, "mode": mode, "analysis": result, "topic": topic, "disclaimer": DISCLAIMER, "timestamp": datetime.datetime.now().isoformat()})

@app.route("/api/pregnancy/month/<int:month>", methods=["GET"])
def pregnancy_month(month):
    if month < 1 or month > 9:
        return jsonify({"error": "Month must be 1-9"}), 400
    provider = request.args.get("provider", "anthropic")
    api_key  = request.args.get("api_key", "")
    effective_key = api_key or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider=="anthropic" else "")
    prompt = f"Provide detailed research for Month {month} of pregnancy (weeks {(month-1)*4+1}-{month*4}). Include: baby development milestones, maternal physical and emotional changes, recommended tests and scans this month, nutrition focus, warning signs to watch for, and preparation advice. Be thorough and compassionate."
    result, mode = call_claude(prompt, provider=provider, api_key=effective_key)
    if not result:
        result = f"Month {month} Pregnancy Research: Detailed information for weeks {(month-1)*4+1}-{month*4}. Please enable live AI for comprehensive month-by-month guidance, or consult your obstetrician."
        mode = "offline"
    return jsonify({"success": True, "mode": mode, "month": month, "content": result, "disclaimer": DISCLAIMER})

@app.route("/api/condition/<condition_name>", methods=["GET"])
def condition_detail(condition_name):
    cn = condition_name.lower().replace("-","_").replace(" ","_")
    if cn in KNOWLEDGE:
        return jsonify({"success": True, "mode": "offline_kb", "condition": KNOWLEDGE[cn], "disclaimer": DISCLAIMER})
    provider = request.args.get("provider", "anthropic")
    api_key  = request.args.get("api_key", "")
    effective_key = api_key or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider=="anthropic" else "")
    prompt = f"Provide comprehensive clinical research about {condition_name} in gynaecology/obstetrics. Include: definition, prevalence, causes, symptoms, diagnosis criteria (with specific investigations and normal ranges), evidence-based treatment options (medical and surgical), prognosis, and management guidelines from ACOG, RCOG, FOGSI."
    result, mode = call_claude(prompt, provider=provider, api_key=effective_key)
    if not result:
        result = build_offline_response(condition_name)
        mode = "offline"
    return jsonify({"success": True, "mode": mode, "content": result, "disclaimer": DISCLAIMER})

@app.route("/api/treatment", methods=["POST"])
def treatment():
    data = request.json or {}
    condition = data.get("condition", "")
    treatment_type = data.get("type", "all")
    provider = data.get("provider", "anthropic")
    api_key  = data.get("api_key", "")
    effective_key = api_key or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider=="anthropic" else "")
    prompt = f"Provide detailed evidence-based treatment research for {condition}. Treatment type focus: {treatment_type}. Include: specific medications with doses, surgical options, alternative treatments, monitoring required, side effects, contraindications, and latest guidelines from ACOG/RCOG/FOGSI."
    result, mode = call_claude(prompt, provider=provider, api_key=effective_key)
    if not result:
        result = build_offline_response(condition)
        mode = "offline"
    return jsonify({"success": True, "mode": mode, "content": result, "disclaimer": DISCLAIMER})

@app.route("/api/scan/interpret", methods=["POST"])
def interpret_scan():
    data = request.json or {}
    scan_type = data.get("scan_type", "Ultrasound")
    findings   = data.get("findings", "")
    context    = data.get("context", "")
    provider = data.get("provider", "anthropic")
    api_key  = data.get("api_key", "")
    effective_key = api_key or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider=="anthropic" else "")
    prompt = f"""
Gynaecological Scan Interpretation Research:
Scan Type: {scan_type}
Reported Findings: {findings}
Clinical Context: {context}

Please research what these findings may indicate, covering:
1. Explanation of each finding in plain English
2. Clinical significance and what differential diagnoses to consider
3. What follow-up investigations may be recommended
4. Questions to ask the reporting radiologist and gynaecologist
5. When findings are urgent vs routine follow-up

IMPORTANT: This is research only. The actual interpretation must be done by the requesting clinician.
"""
    result, mode = call_claude(prompt, provider=provider, api_key=effective_key)
    if not result:
        result = f"Scan interpretation research for {scan_type}. For '{findings}' — this requires clinical correlation by your gynaecologist or radiologist. Please enable live AI for research-based interpretation assistance."
        mode = "offline"
    return jsonify({"success": True, "mode": mode, "content": result, "disclaimer": DISCLAIMER})

@app.route("/api/chat/send", methods=["POST"])
def chat_send():
    data = request.json or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400
    provider = data.get("provider", "anthropic")
    api_key  = data.get("api_key", "")
    effective_key = api_key or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider=="anthropic" else "")
    if data.get("request_ai", False) and is_online() and effective_key:
        prompt = f"A women's health question from a patient: '{message}'\n\nProvide a compassionate, research-based response (3-4 paragraphs). Always end with reminder to consult their gynaecologist."
        result, _ = call_claude(prompt, max_tokens=800, provider=provider, api_key=effective_key)
    else:
        result = None
    return jsonify({"success": True, "ai_response": result, "disclaimer": "Not medical advice. Consult your gynaecologist."})

@app.route("/api/report/generate", methods=["POST"])
def generate_report():
    data = request.json or {}
    topic   = data.get("topic", "General")
    patient = data.get("patient_info", {})
    provider = data.get("provider", "anthropic")
    api_key  = data.get("api_key", "")
    effective_key = api_key or DEFAULT_PROVIDER_KEYS.get(provider, "") or (API_KEY if provider=="anthropic" else "")
    content = build_offline_response(topic, patient_info=patient)
    if effective_key and is_online():
        ai_content, _ = call_claude(f"Generate a comprehensive women's health research report for: {topic}. Patient: {patient}. Cover all aspects including diagnosis, treatment, diet, exercise, emotional health.", max_tokens=3500, provider=provider, api_key=effective_key)
        if ai_content:
            content = ai_content
    report_id = f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    report = {"report_id": report_id, "generated": datetime.datetime.now().isoformat(), "topic": topic, "patient": patient, "content": content, "disclaimer": DISCLAIMER}
    with open(REPORTS_DIR / f"{report_id}.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return jsonify(report)

@app.route("/api/providers", methods=["GET"])
def list_providers():
    """Returns the 5 supported AI providers so the frontend can render a selector."""
    if not AI_PROVIDERS_OK:
        return jsonify({"providers": [], "error": "ai_providers module not available"})
    providers = []
    for key, cfg in ai_providers.PROVIDERS.items():
        providers.append({
            "id": key,
            "label": cfg["label"],
            "default_model": cfg["default_model"],
            "key_prefix": cfg["key_prefix"],
            "get_key_url": cfg["get_key_url"],
            "server_default_configured": bool(DEFAULT_PROVIDER_KEYS.get(key))
        })
    return jsonify({"providers": providers, "online": is_online()})

@app.route("/api/status", methods=["GET"])
def status():
    any_key_configured = bool(API_KEY) or any(DEFAULT_PROVIDER_KEYS.values())
    return jsonify({
        "server": "running", "version": VERSION,
        "online": is_online(),
        "mode": "live_ai" if (any_key_configured and is_online()) else "offline_research",
        "api_key": "configured" if any_key_configured else "not_set",
        "capabilities": {"pdf": FITZ_OK, "images": PIL_OK, "live_ai": bool(any_key_configured and is_online()), "offline": True, "multi_provider": AI_PROVIDERS_OK},
        "knowledge_base": list(KNOWLEDGE.keys()),
        "providers": list(ai_providers.PROVIDERS.keys()) if AI_PROVIDERS_OK else [],
        "disclaimer": DISCLAIMER
    })

# ── Main ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GynoCare AI Server")
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--generate-static", action="store_true")
    args = parser.parse_args()

    if args.generate_static:
        log.info("Static files check complete.")
        sys.exit(0)

    save_knowledge()

    log.info("=" * 60)
    log.info(f"  GynoCare AI Server v{VERSION}")
    log.info("=" * 60)
    log.info(f"  Port:     {args.port}")
    log.info(f"  Online:   {is_online()}")
    log.info(f"  Live AI:  {'YES' if (API_KEY and is_online()) else 'NO (offline/demo mode)'}")
    log.info(f"  Static:   {STATIC_DIR}")
    log.info(f"  Uploads:  {UPLOAD_DIR}")
    log.info("=" * 60)
    log.info(f"  URL: http://localhost:{args.port}")
    log.info("=" * 60)
    log.info(DISCLAIMER)
    log.info("=" * 60)

    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True, use_reloader=False)
