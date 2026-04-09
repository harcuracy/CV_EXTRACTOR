import os
import json
from io import BytesIO
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq


from src.utils.constant import CONFIG_FILE_PATH
from src.utils.helper import read_yaml,create_directories,extract_text,save_json,read_pdf_as_string,docx_to_txt


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")



class CV_EXTRACTOR:

    def __init__(self,config_file_path = CONFIG_FILE_PATH):
        self.config = read_yaml(config_file_path)
        create_directories([self.config.artifact_root])


    def extract(self, file_input):
        """
        Extract text from a resume.
        Accepts:
            - file path (str)
            - in-memory file (BytesIO) with a .name attribute
        Returns extracted text as a string.
        """
        # Determine input type
        if isinstance(file_input, str):
            filename = file_input
            file_bytes = None
        elif isinstance(file_input, BytesIO):
            if not hasattr(file_input, "name"):
                raise ValueError("In-memory file must have a .name attribute")
            filename = file_input.name
            file_bytes = file_input.read()
            file_input.seek(0)
        else:
            raise TypeError("file_input must be str path or BytesIO object")

        # Detect extension
        ext = filename.lower().split(".")[-1]

        # Extract text based on type
        if ext == "pdf":
            text = read_pdf_as_string(BytesIO(file_bytes)) if file_bytes else read_pdf_as_string(filename)
        elif ext == "docx":
            text = docx_to_txt(BytesIO(file_bytes)) if file_bytes else docx_to_txt(filename)
        elif ext == "txt":
            text = file_bytes.decode("utf-8") if file_bytes else extract_text(filename)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return text



    def llm(self):
        Model = ChatGroq(
            model=self.config.LLM.name,
            temperature=self.config.LLM.temperature,
            max_tokens=self.config.LLM.max_tokens,
            timeout=self.config.LLM.timeout,
            max_retries=int(self.config.LLM.max_retries),
            api_key=api_key)
        return Model
    
    def save(self,data:dict):
        save_json(Path(self.config.output),data)

    



       
        



    

