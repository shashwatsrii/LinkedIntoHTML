import openai
from PyPDF2 import PdfReader
from dotenv import load_dotenv

async def process_pdf_to_html(file, api_key):
    openai.api_key = api_key

    reader = PdfReader(file.file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    prompt = f"Please convert the following resume data into a well-structured, professional HTML format. Ensure the HTML output is fully responsive and visually appealing, utilizing inline CSS for styling. The design should be clean, modern, and optimized for both desktop and mobile viewing. The HTML content should be compatible with all major browsers and appear as though it was crafted by a skilled web developer. Focus on creating a layout that is both functional and aesthetically pleasing. Provide only the HTML content enclosed in the body tag, ensuring that there are no errors in the code. Ignore ```html in the response.  \n\nResume : {resume_text}"
    
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "Consider yourself as highly skilled Web Developer."},
            {"role": "user", "content": prompt},
        ],
    )
    print(completion)
    
    resume_html = completion.choices[0].message.content
    return resume_html
