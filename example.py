from tkinterPdfViewer import tkinterPdfViewer as pdf
import tkinter as tk

root = tk.Tk()

v1 = pdf.ShowPdf()
v2 = v1.pdf_view(root, pdf_location="example.pdf", width=100, height=77, dpi=100)
v2.pack()

root.mainloop()