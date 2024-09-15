from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from openai import OpenAI
import os
from starlette.requests import Request

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Function to extract text from PDF and split into chunks
def process_pdf(file):
    pdf_reader = PdfReader(file)
    raw_text = ''
    
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    # Split the text using Character Text Splitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)
    return texts

# Function to generate HTML for resume content
def generate_resume_html(resume_content):
    system_prompt = """
    Generate only the HTML code for the following resume content. Do not include any additional text or explanations.
    Generate an HTML webpage for the following updated resume content. Ensure proper structure with sections like Contact Information, Education, Skills, Experience, Projects, and Coding Platforms. Format the HTML using headings, lists, and sections for clarity and readability.

    Here is the updated resume content: {resume_content}

    The HTML should be clean and styled minimally, using proper elements such as <h1>, <h2>, <ul>, <li>, and <p>. Ensure that each section is well organized and clearly separated.
    """
    
    prompt = system_prompt.format(resume_content=resume_content)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates HTML code for resumes. Generate only the HTML code for the following resume content. Do not include any additional text or explanations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.3
    )
    
    html_code = response.choices[0].message.content.strip()
    return html_code

# FastAPI route for the main page to upload the PDF
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# FastAPI route to handle PDF upload, API key submission, and generate the HTML resume
@app.post("/upload")
async def upload_pdf(request: Request, api_key: str = Form(...), file: UploadFile = File(...)):
    try:
        # Update the OpenAI API key in the environment
        os.environ["OPENAI_API_KEY"] = api_key
        client = OpenAI(api_key=api_key)

        # Process the uploaded PDF
        texts = process_pdf(file.file)

        # Combine extracted text and generate HTML from OpenAI
        extracted_content = "\n".join(texts)
        resume_html = generate_resume_html(extracted_content)

        with open("templates/result.html", "w") as file:
            file.write(resume_html)
    
        return HTMLResponse(content=resume_html, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in processing request: {str(e)}")

