import requests
import json

url = "http://127.0.0.1:5000/resume/generate-pdf"
headers = {"Content-Type": "application/json"}

payload = {
    "personal_info": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "linkedin": "linkedin.com/in/johndoe",
        "github": "github.com/johndoe",
        "role": "Software Engineer"
    },
    "area_of_expertise": [
        "Python",
        "Flask",
        "Streamlit"
    ],
    "key_achievements": [
        "Developed a scalable web application",
        "Optimized database queries"
    ],
    "experience": [
        {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "years": "2020-Present",
            "description": "Developed and maintained web applications."
        }
    ],
    "education": [
        {
            "degree": "M.Sc. Computer Science",
            "university": "University of Example",
            "years": "2018-2020"
        }
    ]
}

try:
    response = requests.post(url, json=payload, timeout=30)

    if response.status_code == 200:
        with open("generated_resume.pdf", "wb") as f:
            f.write(response.content)
        print("PDF generated successfully: generated_resume.pdf")
    else:
        print(f"Error generating PDF: {response.status_code} - {response.text}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}. Make sure the Flask API is running.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")