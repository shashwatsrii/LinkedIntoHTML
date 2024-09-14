import openai
from PyPDF2 import PdfReader

async def process_pdf_to_html(file, api_key):
    openai.api_key = api_key

    reader = PdfReader(file.file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    prompt = f"Please convert the following resume data into a well-structured, professional HTML format. Utilize inline CSS into the tags for the styling of the website. Try to center align most of the things as you could. The design should be clean, modern, and optimized for both desktop and mobile viewing. NOTE: It should definitely look beautiful and optimized. The response you'll give will be directly rendered as HTML, so be precise. Provide only the HTML content enclosed in the body tag, ensuring that there are no errors in the code. Ignore ```html from the response.  \n\nResume : {resume_text}"
    
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
