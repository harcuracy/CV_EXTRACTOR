import os
import yaml
import json
import pypdf
import base64
import tempfile
import docx2txt
from io import BytesIO
from ensure import ensure_annotations
from box.exceptions import BoxValueError
from box import ConfigBox
from pathlib import Path
from typing import Any



from src import logger



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)



@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
    


def write_yaml(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f)
    logger.info(f"yaml file saved at: {path}")

def extract_text(path:str):
    with open(path,"r",encoding="utf-8") as file:
        resume_text = file.read()

        return resume_text


def read_pdf_as_string(file_input):
    """
    Reads a PDF file or in-memory PDF and returns its content as a string.

    Args:
      file_input: str/Path (file path) or BytesIO (in-memory PDF).

    Returns:
      A string containing the content of the PDF file, or None if an error occurs.
    """
    try:
        # If it's a file path
        if isinstance(file_input, (str, os.PathLike)):
            with open(file_input, "rb") as pdf_file:
                pdf_reader = pypdf.PdfReader(pdf_file)
                text = "".join(page.extract_text() for page in pdf_reader.pages)
        else:
            # Assume it's a file-like object (BytesIO)
            pdf_reader = pypdf.PdfReader(file_input)
            text = "".join(page.extract_text() for page in pdf_reader.pages)

        return text

    except FileNotFoundError:
        print(f"Error: File not found at {file_input}")
        return None
    except pypdf.errors.PdfReadError:
        print("Error: Could not read PDF file. It may be corrupted or encrypted.")
        return None



def docx_to_txt(file_input):
    """
    Extract text from a DOCX file or in-memory DOCX file.

    Args:
        file_input: str/Path (file path) or BytesIO (in-memory DOCX).

    Returns:
        text: str
    """
    if isinstance(file_input, (str, os.PathLike)):
        # file path
        text = docx2txt.process(file_input)
        return text
    else:
        # Assume BytesIO object
        # docx2txt only works with file paths, so we need a temporary file
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=True) as tmp_file:
            tmp_file.write(file_input.read())
            tmp_file.flush()
            file_input.seek(0)  # reset pointer
            text = docx2txt.process(tmp_file.name)
        return text
