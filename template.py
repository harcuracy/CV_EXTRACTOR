import os 
from pathlib import Path

project_name = "src"

list_of_files = [

    f"{project_name}/__init__.py",  
    f"{project_name}/cv_processor/__init__.py",
    f"{project_name}/cv_processor/parser.py",
    f"{project_name}/cv_processor/extractor.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/helper.py",
    f"config/config.yaml",
   
    "app.py",
    "requirements.txt",
    "Dockerfile",
    "schema.yaml"

]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir!= "":
        os.makedirs(filedir, exist_ok=True)
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, 'w') as f:
            pass

    else:
        print(f"{filename} is already present in {filedir} and has some content. Skipping creation.")