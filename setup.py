import setuptools

with open("README.md","r") as f:
    long_description = f.read()

setuptools.setup(
  name = 'tkinterPdfViewer',
  version = '0.2',
  license='MIT',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  description = 'The tkinterPdfViewer is python library, which allows you to embed the PDF file in your tkinter GUI',
  author = 'Fahad Devnikar',
  author_email = 'devnikarfahad@gmail.com',
  url = 'https://github.com/Fahad-codecraft',
  keywords = ['PdfViewer', 'tkinter', 'pdf'],
  install_requires=[
          'PyMuPDF',
          'customtkinter',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)