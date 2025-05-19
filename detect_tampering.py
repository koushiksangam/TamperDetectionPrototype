import pdfplumber
import os
from datetime import datetime

def analyzeDocument(filePath):
    results = {
        "filePath": filePath,
        "metadata": {},
        "textInfo": {},
        "flags": []
    }

    if not os.path.exists(filePath):
        results["error"] = "File not found."
        results["flags"].append("FILE_MISSING")
        return results

    try:
        with pdfplumber.open(filePath) as pdf:
            docMetadata = pdf.metadata
            results["metadata"]["raw"] = docMetadata

            createdDate = docMetadata.get('CreationDate')
            modifiedDate = docMetadata.get('ModDate')

            results["metadata"]["Created"] = createdDate
            results["metadata"]["Modified"] = modifiedDate

            if createdDate and modifiedDate:
                if createdDate != modifiedDate:
                     results["flags"].append("DATE_CHANGED")
                     results["metadata"]["dateComparison"] = "Created and Modified dates differ."
                else:
                     results["metadata"]["dateComparison"] = "Created and Modified dates are same."
            elif createdDate:
                 results["metadata"]["dateComparison"] = "Modified date missing."
                 results["flags"].append("MOD_DATE_MISSING")
            elif modifiedDate:
                 results["metadata"]["dateComparison"] = "Created date missing."
                 results["flags"].append("CREATED_DATE_MISSING")
            else:
                 results["metadata"]["dateComparison"] = "Dates missing."
                 results["flags"].append("DATES_MISSING")

            producerName = docMetadata.get('Producer')
            creatorName = docMetadata.get('Creator')
            results["metadata"]["Producer"] = producerName
            results["metadata"]["Creator"] = creatorName

            if not producerName or not creatorName:
                 results["flags"].append("PRODUCER_CREATOR_MISSING")
                 results["metadata"]["producerCreatorCheck"] = "Producer or Creator metadata missing."
            else:
                 results["metadata"]["producerCreatorCheck"] = f"Producer: {producerName}, Creator: {creatorName}"
                 if 'photoshop' in str(producerName).lower() or 'photoshop' in str(creatorName).lower():
                      results["flags"].append("PHOTOSHOP_DETECTED")
                      results["metadata"]["producerCreatorCheck"] += " (Photo editor detected)"

            if len(pdf.pages) > 0:
                pageText = pdf.pages[0].extract_text()
                results["textInfo"]["snippet"] = pageText[:500] + "..." if pageText else "No text."

                keywords = ["university", "degree", "transcript", "certificate"]

                foundKeywords = [keyword for keyword in keywords if keyword.lower() in pageText.lower()]
                results["textInfo"]["foundKeywords"] = foundKeywords

                if not foundKeywords:
                     results["flags"].append("KEYWORDS_MISSING")
                     results["textInfo"]["keywordCheck"] = "Expected keywords not found."
                else:
                     results["textInfo"]["keywordCheck"] = f"Found keywords: {', '.join(foundKeywords)}"

            else:
                results["textInfo"]["status"] = "No pages."
                results["flags"].append("NO_PAGES")

    except Exception as e:
        results["error"] = f"Error processing file: {e}"
        results["flags"].append("PROCESSING_ERROR")

    return results

# --- How to Use ---
# This part runs the analysis.
# It tries to create a simple PDF first (needs 'reportlab' library: pip install reportlab).
# If 'reportlab' is not installed, it will try to analyze a path you give it.

import json

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import os

    def createSimplePdf(name="simple_doc.pdf"):
        c = canvas.Canvas(name, pagesize=letter)
        c.drawString(100, 750, "Sample University Document")
        c.drawString(100, 735, "Student: Test User")
        c.drawString(100, 720, "Degree: Arts")
        c.save()
        print(f"Made simple PDF: {name}")
        return name

    pdfPath = createSimplePdf()

    print("\n--- Checking Simple PDF ---")
    analysisResults = analyzeDocument(pdfPath)
    print(json.dumps(analysisResults, indent=4))

    # os.remove(pdfPath) # Uncomment to delete the simple PDF after checking

except ImportError:
    print("\n'reportlab' not found. Cannot make simple PDF.")
    print("Install it (`pip install reportlab`) or give a path to your own PDF.")
    print("\n--- Checking Your PDF ---")
    # Put the path to your PDF here if reportlab is not installed
    yourPdfPath = "path/to/your/file.pdf" # <--- CHANGE THIS LINE

    analysisResults = analyzeDocument(yourPdfPath)
    print(json.dumps(analysisResults, indent=4))

