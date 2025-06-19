# 💬 GenAI Conversational Bot Platform

This project is a modular GenAI-powered conversational bot platform with support for both a Streamlit-based frontend and an API-based backend.

---

## 📁 Project Structure

```
.
├── app/                    # Core application logic
├── conversation_bot/       # Conversational bot logic and components
├── extras/                 # Optional utilities, prompts, and extras
├── gen_ai/                 # GenAI integration modules (e.g., LLMs, embeddings)
├── generated_images/       # Output folder for generated visual content
├── logs/                   # Runtime logs and metadata
├── notebook/               # Jupyter notebooks for experiments
├── requirements.txt        # Python dependencies
├── sample.env              # Sample environment config (copy to `.env`)
├── scripts/                # Scripts to run the bot locally
├── streamlit_app/          # Streamlit frontend UI components
└── __init__.py             # Package init
```

---

## 🚀 How to Run

### 🖥️ 1. Run the Streamlit App

```bash
python -m streamlit run streamlit_app/main.py
```

This launches the Streamlit UI for interacting with the conversational bot.

---

### 🔌 2. Run the API Version

You’ll need two parts:

#### a. Run the backend (API server):

```bash
python -m app.main
```

#### b. Then run the frontend connected to API:

```bash
python -m streamlit run streamlit_app/app_with_api.py
```

This setup allows the Streamlit frontend to interact with the API backend.

---

### 🤖 3. Run the Bot Locally (Script-based)

You can also use the command-line or script-driven interface from the `scripts/` directory:

```bash
python -m scripts.conversation
```

> *(Make sure to check script names, adjust accordingly.)*

---

## 🛠️ Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

2. **Create virtual environment and activate**

```bash
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate     
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables**

`sample.env`  fill in your keys/config:


---

## 🧪 Development Notes

- Logs are stored in the `logs/` directory.
- Generated images are saved in `generated_images/`.
- Notebooks are available under `notebook/` for experimentation.

