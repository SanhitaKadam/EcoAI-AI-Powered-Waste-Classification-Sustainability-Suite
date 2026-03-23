# ♻️ EcoAI – AI-Powered Waste Classification & Sustainability Suite

> Powered by **Meta Llama 3.2 (3B)** running locally via **Ollama** + **Streamlit**

---

## 🚀 Setup in VS Code (Step-by-Step)

### 1. Install Ollama
Download from https://ollama.com and install it.

Then open a terminal and pull the model:
```bash
ollama pull llama3.2
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
Make sure Ollama is running (it starts automatically after install, or run `ollama serve`), then:
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 📁 Project Structure
```
waste_classifier/
├── app.py                  ← Main Streamlit app
├── requirements.txt        ← Python dependencies
├── .streamlit/
│   └── config.toml         ← Streamlit theme config
└── README.md
```

---

## ✨ Features
- 🔍 **AI Waste Classification** — Plastic, Metal, Organic, E-Waste, Glass, Paper, Hazardous
- 💡 **DIY Upcycling Ideas** — 3 creative reuse suggestions per item
- 🌍 **CO₂ Impact Estimate** — Shows estimated CO₂ saved by recycling
- 📜 **Classification History** — Session-based log of all classified items
- 📚 **Disposal Guide** — Reference guide for all waste categories
- 📊 **Session Stats** — Total classified, recyclable count, CO₂ saved

---

## 🛠️ Tech Stack
| Layer | Tech |
|-------|------|
| LLM | Meta Llama 3.2 3B (local) |
| Inference | Ollama |
| Frontend | Streamlit |
| Language | Python 3.10+ |

---

## 🐛 Troubleshooting

**"Ollama not running" error**
```bash
ollama serve
```

**Model not found**
```bash
ollama pull llama3.2
```

**Slow responses?**
- Use `llama3.2:1b` (1B parameter model) for faster inference on low-end hardware:
  ```bash
  ollama pull llama3.2:1b
  ```
  Then select it from the sidebar dropdown.
