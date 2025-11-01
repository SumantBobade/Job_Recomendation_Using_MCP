# import fitz # PyMuPDF
# import os
# from dotenv import load_dotenv  # For loading environment variables
# from openai import OpenAI  # OpenAI API client

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# client = OpenAI(api_key=OPENAI_API_KEY)


# def extract_text_from_pdf(uploder_file):
#     """
#     Extracts text from a PDF file.

#     Args:
#         uploder_file: The uploaded PDF file.
#     Returns:
#         str: The extracted text from the PDF.
#     """
#     doc = fitz.open(stream=uploder_file.read(), filetype="pdf")
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# def ask_openai(prompt, max_tokens=500):
#     """
#     Send a prompt to OpenAI's API and get a response.
#     Args:
#         prompt (_type_): _description_
#         max_tokens (int, optional): _description_. Defaults to 500.
        
#     Returns:
#         str: The response from OpenAI's API.
#     """
    
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "user", 
#              "content": prompt
#             }
#         ],
#         temperature= 0.5,
#         max_tokens=max_tokens,
#     )
#     return response.choices[0].message.content


import fitz  # PyMuPDF
from transformers import pipeline

# Load a free model from Hugging Face
generator = pipeline("text2text-generation", model="google/flan-t5-large")


def extract_text_from_pdf(uploader_file):
    """
    Extracts text from a PDF file.
    """
    doc = fitz.open(stream=uploader_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_model(prompt, max_tokens=250):
    """
    Uses a free Hugging Face model instead of OpenAI. For getting resume summaries and analyses. And find key isights and keywords.
    """
    response = generator(prompt, max_length=max_tokens, num_return_sequences=1)
    return response[0]['generated_text']
