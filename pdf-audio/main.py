import os

import pyttsx3
import PyPDF2
from sys import argv

path = argv[1]
save_in = os.curdir

# insert name of your pdf
pdfreader = PyPDF2.PdfReader(open(path, 'rb'))
speaker = pyttsx3.init()
texts = ""

for page_num in range(len(pdfreader.pages)):
    text = pdfreader.pages[page_num].extract_text()
    clean_text = text.strip().replace('\n', ' ')
    texts += clean_text

# name mp3 file whatever you would like
print(texts)
speaker.save_to_file(texts, f'{save_in}/story.mp3')
speaker.runAndWait()

speaker.stop()
