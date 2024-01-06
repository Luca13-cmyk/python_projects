import os
from PyPDF2 import PdfMerger, PdfReader
import sys
merger = PdfMerger()
for file in os.listdir(os.curdir):
    if file.endswith(".pdf"):
        merger.append(PdfReader(file))

merger.write("combinedDocs.pdf")


