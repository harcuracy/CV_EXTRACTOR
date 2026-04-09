from src.utils.helper import read_yaml
from src.utils.constant import SCHEMA_FILE_PATH


CV_SCHEMA = dict(read_yaml(SCHEMA_FILE_PATH))

def build_prompt(resume_text: str):
    prompt_template = f"""
You are an expert resume parser.

Return ONLY valid JSON.

Rules:
- No explanation
- No markdown
- Never invent information
- If data is missing, return empty values
- Summary about the user project 
- Make the output a double ""

Schema:
{{CV_SCHEMA}}


Resume:
{{resume_text}}

"""
    return  prompt_template