import os
from PyPDF2 import PdfReader


def allowed_file(filename):
    """
    Check whether the uploaded file is a PDF.
    """
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() == "pdf"
    )


def validate_pdf(file):
    """
    Validate uploaded PDF.
    """
    if file is None:
        return False

    if file.filename == "":
        return False

    return allowed_file(file.filename)


def extract_pdf_text(file_path):
    """
    Extract text from PDF.
    """
    try:
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        print("PDF Error:", e)
        return ""


def get_pdf_details(file_path):
    """
    Return PDF information.
    """
    try:
        reader = PdfReader(file_path)

        return {
            "pages": len(reader.pages),
            "size_kb": round(
                os.path.getsize(file_path) / 1024,
                2
            )
        }

    except Exception:
        return {
            "pages": 0,
            "size_kb": 0
        }


if __name__ == "__main__":
    print("PDF Processor Ready")