import openai
from PyPDF2 import PdfReader

async def process_pdf_to_html(file, api_key):
    try:
        openai.api_key = api_key

        reader = PdfReader(file.file)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text()

        prompt = f'''Please convert the following resume data into a well-structured, professional HTML format. Utilize inline CSS into the tags for the styling of the website. Try to align the html according to the styling. The design should be clean, modern, and optimized for both desktop and mobile viewing. NOTE: It should definitely look beautiful and optimized. The response you'll give will be directly rendered as HTML, so be precise. Provide only the HTML content enclosed in the body tag, ensuring that there are no errors in the code. 
        Please follow the structure : Name, Contact, Summary, Experience, Projects, Language, Skills, Achievements Ignore ```html from the response.  \n\nResume : {resume_text}'''
        
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

    except Exception as e:
        error_html = f'''<html>
                            <body style='display: flex; justify-content: center; align-items: center;'>
                                <h1>Error: Open AI API Key Invalid.</h1>
                                <a href='/'>Go back to home </a>
                            </body>
                        </html>'''
        return error_html