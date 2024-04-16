# tkPDFViewer

[Powered by [Roshan]](https://github.com/Roshanpaswan/PdfViewer)

The tkPDFViewer is python library, which allows you to embed the PDF file in your tkinter GUI. In just three steps.

  - Install
  - Import
  - Embed on your gui

# Features!

  - Embed your PDF in your tkinter GUI.
  - Customize width and height of your PDF.
  - Zoom in and zoom out you pdf with shortcuts like ctrl+mousewheel or ctrl+ or ctrl-
  - Open Encrypted PDFs

> High quality pdf pages image
> with customizable width and height
> worked with python 3.0+.

### Installation


Install tkPDFViewer using pip

```sh
pip install tkinterPdfViewer
```


Install tkPDFViewer using pip3

```sh
pip3 install tkinterPdfViewer
```

### Usage

An Example of Using tkinterPdfViewer.

```sh
from tkinterPdfViewer import tkinterPdfViewer as pdf
import tkinter as tk

root = tk.Tk()
root.geometry("700x780")
d = pdf.ShowPdf().pdf_view(root, pdf_location=r"location", width=100, height=100)
d.pack()
root.mainloop()

```


### Attributes

```sh
pdf_location = "" --> location of your pdf
```

```sh
width = 0 --> width of your pdf to be embeded
```

```sh
height = 0 --> height of your pdf to be embeded
```

```sh
To embed your pdf use --> .pack() or .grid() or .place()
```

```sh
bar --> True or False, Through this attribute you can hide or unhide the loading bar which showing on the frame after your gui is opened. This indicate that 'how much your pdf is loaded'.Once it complete it unhide automatically and your pdf get embeded.
```

```sh
load --> after or before, Through this attribute you can decide that , when your pdf object is to convert. If you select 'after' then the object of your pdf is convert after your gui is opened.Otherwise it convert first then your gui is opened. It is recommended that to select after which is default.Beacause this takes time. Depends on the size of pdf. And if you select 'before' then it make your gui slow to open. 
```

```sh
dpi --> change dpi of the pdf to show
```




# Dependencies

 - tkinter
 - PyMuPDF
 - Thread
 - math
 - customtkinter


License
----

MIT

# Author

 - [Fahad Devnikar](https://github.com/Fahad-codecraft/)
 