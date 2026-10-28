import pymupdf

with pymupdf.open("example2.pdf") as doc:
    text = doc[0].get_text("text")
print(text)