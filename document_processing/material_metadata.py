material = {
    "title": "Data Cleaning",
    "file": "Data_Cleaning.pdf",
    "topics": [
        "Missing Values",
        "Duplicate Records",
        "Incorrect Data",
        "Inconsistent Formats",
        "Outliers",
        "Standardization",
        "Validation",
        "Data Quality",
        "Data Cleaning"
    ]
}

print("Learning Material:")
print("Title:", material["title"])
print("File:", material["file"])
print("Topics:")

for topic in material["topics"]:
    print("-", topic)