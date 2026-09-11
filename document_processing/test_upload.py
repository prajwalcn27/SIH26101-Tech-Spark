import requests
import os


url = "http://127.0.0.1:5000/upload-material"


# Project root
base_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)


# PDF location
pdf_path = os.path.join(
    base_dir,
    "learning_materials",
    "Data_Cleaning.pdf"
)


print("PDF path:")
print(pdf_path)


if not os.path.exists(pdf_path):
    print("ERROR: PDF file not found!")
    exit()


with open(pdf_path, "rb") as pdf_file:

    files = {
        "file": (
            "Data_Cleaning.pdf",
            pdf_file,
            "application/pdf"
        )
    }

    response = requests.post(
        url,
        files=files
    )


print("\nStatus Code:", response.status_code)

print("\nResponse:")

print(response.json())