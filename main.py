import json
from io import BytesIO
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.cv_processor.prompt_builder import build_prompt, CV_SCHEMA
from src.cv_processor.extractor import CV_EXTRACTOR

parser = StrOutputParser()

def main(file_like: BytesIO):
    """
    Process a CV in memory and return structured JSON data.
    """
    if not hasattr(file_like, "name"):
        raise ValueError("BytesIO object must have a .name attribute with file extension")

    cv_extractor = CV_EXTRACTOR()
    resume_text = cv_extractor.extract(file_like)
    llm = cv_extractor.llm()

    my_chain = PromptTemplate(
        input_variables=["CV_SCHEMA", "resume_text"],
        template=build_prompt(resume_text)
    ) | llm | parser

    message = my_chain.invoke({"CV_SCHEMA": CV_SCHEMA, "resume_text": resume_text})

    try:
        data_dict = json.loads(str(message))
    except json.JSONDecodeError:
        raise ValueError("LLM output could not be parsed as JSON")

    cv_extractor.save(data_dict)
    return data_dict