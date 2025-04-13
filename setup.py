from setuptools import setup, find_packages

setup(
    name="my_jd_extraction_api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic",
        "pydantic-settings",
        "uvicorn",
        "python-multipart",
        "openai",
        "httpx",
        "PyPDF2",
        "python-docx",
        "pillow",
        "pytesseract",
        "lxml",
    ],
    python_requires=">=3.8",
) 