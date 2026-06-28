import PyPDF2
import logging


logging.basicConfig(level=logging.INFO)


def extract_text_from_pdf(pdf_path):

    text = ""

    try:
        with open(pdf_path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        logging.info(f"Successfully extracted {pdf_path}")

    except Exception as e:

        logging.error(
            f"Error extracting {pdf_path}: {e}"
        )

    return text