import os
import json
import PyPDF2
import pandas as pd

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading the PDF file.")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsuppored file format. Only .pdf and .txt files are supported.")
    

def output_dataframe(json_string):
    try:
        json_object = json.loads(json_string)
        json_data = json_object['data']
        df = pd.DataFrame(json_data)
        return df
    except Exception as e:
        raise ValueError("Error converting JSON to DataFrame.") from e

def output_file(output_data, output_folder, output_file_name):
    if output_file_name.endswith(".csv"):
        try:
            # Construct the file path using string formatting
            file_path = os.path.join(output_folder, output_file_name)
            output_data.to_csv(file_path, index=False)
        except Exception as e:
            raise ValueError("Error writing DataFrame to CSV file.") from e
    elif output_file_name.endswith(".txt"):
        try:
            # Construct the file path using string formatting
            file_path = os.path.join(output_folder, output_file_name)
            with open(file_path, 'w') as output_file:
                output_file.write(output_data)
        except Exception as e:
            raise ValueError("Error writing JSON to text file.") from e