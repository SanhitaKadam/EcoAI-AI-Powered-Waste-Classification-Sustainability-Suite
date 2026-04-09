import streamlit as st
import ollama
import json
import time
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EcoAI – Waste Classifier",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1f1a 50%, #0a1510 100%);
    color: #e8f5e2;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(10, 30, 20, 0.95) !important;
    border-right: 1px solid #1e4d30;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
    letter-spacing: -0.5px;
}

/* Main title */
.main-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4ade80, #86efac, #bbf7d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 0.2rem;
}

.sub-title {
    color: #6b9e7a;
    font-size: 0.95rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Cards */
.eco-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(74, 222, 128, 0.15);
    border-radius: 12px;
    padding: 1.4rem;
    margin: 0.8rem 0;
    backdrop-filter: blur(10px);
}

.eco-card-accent {
    background: rgba(74, 222, 128, 0.06);
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 12px;
    padding: 1.4rem;
    margin: 0.8rem 0;
}

/* Category badges */
.badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.badge-plastic  { background: #1e3a5f; color: #60a5fa; border: 1px solid #3b82f6; }
.badge-metal    { background: #2d2d1e; color: #fbbf24; border: 1px solid #f59e0b; }
.badge-organic  { background: #1a3320; color: #4ade80; border: 1px solid #22c55e; }
.badge-ewaste   { background: #3b1f3b; color: #e879f9; border: 1px solid #d946ef; }
.badge-glass    { background: #1e3a4a; color: #67e8f9; border: 1px solid #06b6d4; }
.badge-paper    { background: #3b2d1e; color: #fb923c; border: 1px solid #f97316; }
.badge-hazardous{ background: #3b1e1e; color: #f87171; border: 1px solid #ef4444; }
.badge-unknown  { background: #2a2a2a; color: #9ca3af; border: 1px solid #6b7280; }

/* Metrics */
.metric-box {
    background: rgba(74, 222, 128, 0.05);
    border: 1px solid rgba(74, 222, 128, 0.2);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-number {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #4ade80;
}
.metric-label {
    font-size: 0.75rem;
    color: #6b9e7a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Input */
.stTextArea textarea {
    background: rgba(10,25,15,0.8) !important;
    border: 1px solid rgba(74,222,128,0.3) !important;
    border-radius: 10px !important;
    color: #e8f5e2 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 2px rgba(74,222,128,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #166534, #15803d) !important;
    color: #dcfce7 !important;
    border: 1px solid #22c55e !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #15803d, #16a34a) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(74,222,128,0.25) !important;
}

/* Divider */
hr { border-color: rgba(74,222,128,0.15) !important; }

/* Spinner */
.stSpinner > div { border-top-color: #4ade80 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e4d30; border-radius: 10px; }

/* Result section */
.result-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #4ade80;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.4rem;
}

.tip-box {
    background: rgba(250, 204, 21, 0.05);
    border-left: 3px solid #fbbf24;
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    color: #fef9c3;
}

.history-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(74,222,128,0.1);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "total_classified" not in st.session_state:
    st.session_state.total_classified = 0
if "model_ready" not in st.session_state:
    st.session_state.model_ready = False

# ─── Constants ───────────────────────────────────────────────────────────────
CATEGORY_BADGES = {
    "Plastic":   "badge-plastic",
    "Metal":     "badge-metal",
    "Organic":   "badge-organic",
    "E-Waste":   "badge-ewaste",
    "Glass":     "badge-glass",
    "Paper":     "badge-paper",
    "Hazardous": "badge-hazardous",
    "Unknown":   "badge-unknown",
}

CATEGORY_ICONS = {
    "Plastic":   "🧴",
    "Metal":     "🔩",
    "Organic":   "🍃",
    "E-Waste":   "💻",
    "Glass":     "🫙",
    "Paper":     "📄",
    "Hazardous": "⚠️",
    "Unknown":   "❓",
}

DISPOSAL_TIPS = {
    "Plastic":   "Rinse before recycling. Check the resin code (1–7) on the bottom. Hard plastics → blue bin. Soft plastics → drop-off point.",
    "Metal":     "Aluminium & steel are infinitely recyclable. Crush cans to save space. Remove food residue first.",
    "Organic":   "Compost at home or use municipal green-waste bins. Avoid meat/dairy in home composters.",
    "E-Waste":   "Never in general waste. Use certified e-waste recyclers or manufacturer take-back programs.",
    "Glass":     "Separate by colour (clear, green, brown). Rinse thoroughly. Broken glass — wrap safely before disposal.",
    "Paper":     "Keep dry. Remove plastic windows from envelopes. Shredded paper may need separate handling.",
    "Hazardous": "Do NOT put in regular bins. Use local hazardous-waste collection events or approved drop-offs.",
    "Unknown":   "When in doubt, research the specific material or take it to a waste sorting facility.",
}

SYSTEM_PROMPT = """You are EcoAI, an expert waste classification and sustainability consultant.

When given a waste item description, you MUST respond in valid JSON with this exact structure:
{
  "category": "<one of: Plastic, Metal, Organic, E-Waste, Glass, Paper, Hazardous, Unknown>",
  "confidence": "<High/Medium/Low>",
  "item_name": "<clean name of the item>",
  "recyclable": true/false,
  "co2_saved_kg": <estimated kg of CO2 saved by recycling, as a number>,
  "upcycling_ideas": [
    "<idea 1>",
    "<idea 2>",
    "<idea 3>"
  ],
  "fun_fact": "<one short, interesting environmental fact about this type of waste>",
  "disposal_steps": [
    "<step 1>",
    "<step 2>"
  ]
}

Be accurate, practical, and encouraging. Return ONLY the JSON — no preamble, no extra text."""


def classify_waste(item_description: str, model: str = "llama3.2") -> dict:
    """Call local Ollama model and parse JSON response."""
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Classify this waste item: {item_description}"},
            ],
        )
        raw = response["message"]["content"].strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {"error": "Could not parse AI response. Try rephrasing your input."}
    except Exception as e:
        return {"error": str(e)}


def check_ollama_models() -> list:
    """Return list of available local Ollama models."""
    try:
        models = ollama.list()
        return [m["name"] for m in models.get("models", [])]
    except Exception:
        return []


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ♻️ EcoAI Settings")
    st.markdown("---")

    available_models = check_ollama_models()
    preferred = [m for m in available_models if "llama3.2" in m or "llama3" in m]
    default_models = preferred if preferred else (available_models if available_models else ["llama3.2"])

    if available_models:
        selected_model = st.selectbox(
            "🤖 LLM Model",
            options=default_models + [m for m in available_models if m not in default_models],
            help="Select the local Ollama model to use.",
        )
        st.success(f"✅ Ollama connected — {len(available_models)} model(s) found")
    else:
        selected_model = "llama3.2"
        st.error("⚠️ Ollama not running. Start it with:\n```\nollama serve\n```")
        st.info("Then pull the model:\n```\nollama pull llama3.2\n```")

    st.markdown("---")
    st.markdown("### 📊 Session Stats")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">{st.session_state.total_classified}</div>
            <div class="metric-label">Classified</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        recyclable_count = sum(1 for h in st.session_state.history if h.get("recyclable"))
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">{recyclable_count}</div>
            <div class="metric-label">Recyclable</div>
        </div>""", unsafe_allow_html=True)

    total_co2 = sum(float(h.get("co2_saved_kg") or 0) for h in st.session_state.history)
    st.markdown(f"""
    <div class="metric-box" style="margin-top:0.6rem">
        <div class="metric-number">{total_co2:.2f}</div>
        <div class="metric-label">kg CO₂ Saved (est.)</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.total_classified = 0
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#4a7a5a; line-height:1.6;">
    <b>Stack</b><br>
    🦙 Meta Llama 3.2 (3B)<br>
    🌐 Streamlit<br>
    🔗 Ollama (local inference)<br>
    🐍 Python 3.10+
    </div>
    """, unsafe_allow_html=True)

# ─── Main ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">♻ EcoAI Waste Classifier</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Powered Waste Segregation & Sustainability Suite</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 Classify Waste", "📜 History", "📚 Disposal Guide"])

# ── Tab 1: Classify ───────────────────────────────────────────────────────────
with tab1:
    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown('<div class="eco-card">', unsafe_allow_html=True)
        st.markdown("#### 📝 Describe Your Waste Item")
        st.markdown("Be specific — material, size, condition all help!")

        user_input = st.text_area(
            label="",
            placeholder="e.g. 'Empty aluminium cola can', 'Old smartphone with cracked screen', 'Banana peel', 'Broken wine bottle'...",
            height=130,
            label_visibility="collapsed",
        )

        examples = ["Empty plastic water bottle", "Dead AA batteries", "Coffee grounds", "Old laptop charger", "Cardboard box", "Glass jam jar"]
        st.markdown("**Quick examples:**")
        ex_cols = st.columns(3)
        for i, ex in enumerate(examples):
            with ex_cols[i % 3]:
                if st.button(ex, key=f"ex_{i}", use_container_width=True):
                    user_input = ex

        classify_btn = st.button("⚡ Classify Now", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        if classify_btn and user_input.strip():
            with st.spinner("🔬 Analysing with EcoAI..."):
                result = classify_waste(user_input.strip(), model=selected_model)

            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                st.session_state.total_classified += 1
                result["input"] = user_input.strip()
                result["timestamp"] = datetime.now().strftime("%H:%M:%S")
                st.session_state.history.insert(0, result)

                cat = result.get("category", "Unknown")
                badge_cls = CATEGORY_BADGES.get(cat, "badge-unknown")
                icon = CATEGORY_ICONS.get(cat, "❓")

                st.markdown(f"""
                <div class="eco-card-accent">
                    <div class="result-header">Classification Result</div>
                    <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.8rem;">
                        <span style="font-size:2rem">{icon}</span>
                        <div>
                            <span style="font-size:1.4rem; font-weight:700; color:#e8f5e2;">{result.get("item_name", user_input)}</span><br>
                            <span class="badge {badge_cls}">{cat}</span>
                            &nbsp;
                            <span class="badge" style="background:rgba(255,255,255,0.05);color:#9ca3af;border:1px solid #374151;">
                                {result.get("confidence","?")} confidence
                            </span>
                        </div>
                    </div>
                    <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:0.8rem;">
                        <span style="color:{'#4ade80' if result.get('recyclable') else '#f87171'}; font-size:0.9rem;">
                            {"✅ Recyclable" if result.get('recyclable') else "❌ Not Recyclable"}
                        </span>
                        <span style="color:#fbbf24; font-size:0.9rem;">
                            🌍 ~{float(result.get("co2_saved_kg") or 0):.2f} kg CO₂ saved
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if result.get("upcycling_ideas"):
                    st.markdown("**💡 DIY Upcycling Ideas:**")
                    for idea in result["upcycling_ideas"]:
                        st.markdown(f"""<div class="tip-box">💚 {idea}</div>""", unsafe_allow_html=True)

                if result.get("disposal_steps"):
                    with st.expander("🗑️ Disposal Steps"):
                        for i, step in enumerate(result["disposal_steps"], 1):
                            st.markdown(f"**{i}.** {step}")

                if result.get("fun_fact"):
                    st.info(f"🌿 **Eco Fact:** {result['fun_fact']}")

        elif classify_btn:
            st.warning("Please describe a waste item first.")
        else:
            st.markdown("""
            <div class="eco-card" style="text-align:center; padding:2rem; opacity:0.6;">
                <div style="font-size:3rem">🌿</div>
                <div style="font-family:'Space Mono',monospace; font-size:0.85rem; color:#4a7a5a; margin-top:0.5rem;">
                    Enter a waste item to get started
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Tab 2: History ────────────────────────────────────────────────────────────
with tab2:
    if not st.session_state.history:
        st.markdown("""
        <div class="eco-card" style="text-align:center; padding:2rem; opacity:0.5;">
            <div style="font-size:2.5rem">📜</div>
            <div style="font-family:'Space Mono',monospace; font-size:0.85rem; color:#4a7a5a; margin-top:0.5rem;">
                No history yet — classify some items!
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        for entry in st.session_state.history:
            cat = entry.get("category", "Unknown")
            icon = CATEGORY_ICONS.get(cat, "❓")
            badge_cls = CATEGORY_BADGES.get(cat, "badge-unknown")
            st.markdown(f"""
            <div class="history-item">
                <span style="font-size:1.1rem">{icon}</span>
                <span style="font-weight:600; color:#e8f5e2; margin:0 0.5rem;">{entry.get("item_name", entry.get("input","?"))}</span>
                <span class="badge {badge_cls}">{cat}</span>
                &nbsp;
                <span style="color:#6b9e7a; font-size:0.75rem; float:right;">{entry.get("timestamp","")}</span>
            </div>""", unsafe_allow_html=True)

# ── Tab 3: Disposal Guide ─────────────────────────────────────────────────────
with tab3:
    st.markdown("#### 🗑️ Quick Disposal Reference Guide")
    for cat, tip in DISPOSAL_TIPS.items():
        icon = CATEGORY_ICONS.get(cat, "❓")
        badge_cls = CATEGORY_BADGES.get(cat, "badge-unknown")
        with st.expander(f"{icon}  {cat}"):
            st.markdown(f"""<span class="badge {badge_cls}">{cat}</span>""", unsafe_allow_html=True)
            st.markdown(f"\n\n{tip}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#2d5a3d; font-size:0.75rem; font-family:'Space Mono',monospace; padding:0.5rem 0;">
    EcoAI • Powered by Meta Llama 3.2 • Running locally via Ollama
</div>
""", unsafe_allow_html=True)