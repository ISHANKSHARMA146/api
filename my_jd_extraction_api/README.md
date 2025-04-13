# Job Description Extraction & Enhancement API

A standalone API for extracting structured information from job description files and enhancing them with additional details.

## Features

- **File Parsing**: Extract text from PDF, DOCX, and image files
- **Structured Extraction**: Convert raw text into structured job description data
- **Enhancement**: Enrich job descriptions with additional details and improved formatting
- **Comprehensive Schema**: Detailed schema covering all aspects of job descriptions
- **RESTful API**: Simple and easy-to-use REST API endpoints

## API Endpoints

### Extraction Endpoint

`POST /extraction/`

Accepts a file upload (PDF, DOCX, or image) and returns a structured job description.

**Request**:
- Content-Type: multipart/form-data
- Body: file

**Response**:
```json
{
  "extracted_jd": {
    "basic_info": { ... },
    "posting_metadata": { ... },
    "role_description": { ... },
    "requirements": { ... },
    "skills": { ... },
    "compensation": { ... },
    "work_environment": { ... },
    "career_path": { ... },
    "original_text": "..."
  },
  "message": "Job description extracted successfully"
}
```

### Enhancement Endpoint

`POST /enhancement/`

Accepts a structured job description (from the extraction endpoint) and returns an enhanced version.

**Request**:
- Content-Type: application/json
- Body:
```json
{
  "extracted_jd": {
    "basic_info": { ... },
    "posting_metadata": { ... },
    ...
  }
}
```

**Response**:
```json
{
  "enhanced_jd": {
    "basic_info": { ... },
    "posting_metadata": { ... },
    "role_description": { ... },
    "requirements": { ... },
    "skills": { ... },
    "compensation": { ... },
    "work_environment": { ... },
    "career_path": { ... },
    "original_text": "..."
  },
  "message": "Job description enhanced successfully"
}
```

## Setup & Deployment

### Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install the package in development mode:
   ```
   pip install -e .
   ```
5. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
6. Run the application using the run script:
   ```
   python run.py
   ```

### Deployment on Vercel

1. Fork this repository to your GitHub account
2. Connect your repository to Vercel
3. Add the environment variable `OPENAI_API_KEY` with your OpenAI API key
4. Update the Vercel configuration if needed
5. Deploy!

## Schema

The API uses a comprehensive schema to structure job descriptions, including:

- Basic Job Info (title, code, level, department, category)
- Job Posting Metadata (contract duration, time commitment)
- Detailed Role Description (summary, tasks, KPIs, decision-making, stakeholders)
- Requirements (qualifications, certifications, legal eligibility)
- Skills Classification (hard skills, soft skills, domain expertise, methodologies)
- Compensation Details (salary, bonus, equity, benefits)
- Work Environment (work model, locations, travel)
- Career Path Information (growth opportunities, training programs)

## License

MIT 