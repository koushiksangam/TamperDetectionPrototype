# TamperDetectionPrototype

# Simple PDF Checker (Metadata Detective!)

Hey there! 👋

This is just a small project I put together for an assignment. Basically, it's a simple tool that looks at a PDF file to find some basic clues if it might have been messed with.

Think of it like a quick check of the PDF's "birth certificate" and first page.

**What this code checks:**

* **Hidden Info (Metadata):** It looks at information hidden inside the PDF, like when it was made and when it was last changed. If these dates look odd, or if it sees software names usually used for photo editing (like Photoshop) in the history, it raises a little flag.
* **First Page Text:** It reads the text on the very first page and checks if some common words you'd expect in a document (like "university" or "degree") are there. If they are missing, that could be a bit strange.

It's just a basic check, not a full-on FBI investigation! 😉

**Wanna try running it?**

Here are the simple steps:

1.  Make sure you have Python installed on your computer.
2.  Open your terminal or command prompt (that black window).
3.  Go to the folder where you saved this code file (`.py` file).
4.  You need one main helper tool for this code: `pdfplumber`. Type this command and press Enter:
    ```bash
    pip install pdfplumber
    ```
5.  (Optional) If you want the code to make a simple test PDF for you automatically, you also need the `reportlab` helper. Type this command and press Enter:
    ```bash
    pip install reportlab
    ```
6.  Open the Python code file (`.py` file) in VS Code or a text editor.
7.  Go to the very bottom of the file. There's a section that shows how to run the code.
    * If you installed `reportlab`, it will automatically create and check a dummy PDF.
    * If you didn't install `reportlab`, it will try to check a file path written in the code. You can change this path (`"path/to/your/file.pdf"`) to point to any PDF file you want to check.
8.  Save the file after changing the path (if you did).
9.  Now, run the code! In the terminal (make sure you are in the right folder!), type:
    ```bash
    python your_code_file_name.py
    ```
    (Replace `your_code_file_name.py` with the actual name of your Python file).

The code will print some information and a list of "flags" (like `DATE_CHANGED` or `KEYWORDS_MISSING`) if it found anything suspicious based on its basic checks.

That's it! It's a simple start to catching fake documents.

Hope this helps! ✨
