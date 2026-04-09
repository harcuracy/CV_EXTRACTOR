# CV_EXTRACTOR

A Python-based tool that extracts structured information from resumes using AI. Built with **FastAPI**, **LangChain**, and **Groq API**, it converts uploaded CVs into structured JSON according to a predefined schema.

---

## Features

- Upload a resume in PDF, DOCX, or TXT format.  
- Extract key information: name, contact info, skills, education, experience, etc.  
- Return data in JSON format for easy integration.  
- Built-in LLM integration for intelligent parsing.  

---

## Tech Stack

- **Python 3.10+**  
- **FastAPI** – Web framework  
- **LangChain** – LLM orchestration  
- **Groq API** – Language model backend  
- **Uvicorn** – ASGI server  
- **Docker** – Containerization (optional)  

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/harcuracy/CV_EXTRACTOR.git
cd CV_EXTRACTOR 
```

### 2. Install UV With PIP

```bash
pip install uv
```

### 3. Install Environment Variable With Python Version

```bash
uv venv --python 3.10
```

### 4. Activate the Environment Variable

```bash
.venv\Scripts\activate
```

### 5. Install The Requirements File

```bash
uv pip install -r requirements.txt
```

### 6. Set GROQ API TO ENVIRONMENT

```bash
# Windows CMD
set GROQ_API_KEY=your_api_key_here

# Mac/Linux
export GROQ_API_KEY=your_api_key_here

```

### 7. Run the Python File

```bash
python app.py
```

## License

This project is licensed under MIT License.