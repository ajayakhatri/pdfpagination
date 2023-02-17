import os
import PyPDF2
from fpdf import FPDF


dir_path = r'pdf'
pdfn=(len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))
pdfn
totalpages=0
for pdfname in range(pdfn):
    inputFile = PyPDF2.PdfReader(f"pdf/{pdfname+1}.pdf")
    totalpages=totalpages+len(inputFile.pages)
print(totalpages)


global count
global pdfpagecount
count=0
class NumberPDF(FPDF):
    def __init__(self, numberOfPages):
        super(NumberPDF, self).__init__()
        self.numberOfPages = numberOfPages
    # Overload Header
    def header(self):
        pass

    # Overload Footer
    def footer(self):
        pagenumber=count-pdfpagecount+self.page_no()
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 11
        self.set_font("helvetica", "I", 11)
        # Printing page number:
        self.cell(0, 10, f"Page {pagenumber} of {totalpages}" , align="C")
        
for pdfname in range(pdfn):
    # Grab the file you want to add pages to
    inputFile = PyPDF2.PdfReader(f"pdf/{pdfname+1}.pdf")
    outputFile = (f"unmergedpdfs/{pdfname+1}.pdf")

    count=count+len(inputFile.pages)
    pdfpagecount=len(inputFile.pages)

    # Create a temporary numbering PDF using the overloaded FPDF class, passing the number of pages
    # from your original file
    tempNumFile = NumberPDF(len(inputFile.pages))

    # Add a new page to the temporary numbering PDF (the footer function runs on add_page and will 
    # put the page number at the bottom, all else will be blank
    for page in range(len(inputFile.pages)):
        tempNumFile.add_page()


    # Save the temporary numbering PDF
    tempNumFile.output("tempNumbering.pdf")

    # Create a new PDFFileReader for the temporary numbering PDF
    mergeFile = PyPDF2.PdfReader("tempNumbering.pdf")

    # Create a new PDFFileWriter for the final output document
    mergeWriter = PyPDF2.PdfWriter()

    # Loop through the pages in the temporary numbering PDF
    for x, page in enumerate(mergeFile.pages):

        # Grab the corresponding page from the inputFile
        inputPage = inputFile.pages[x]

        # Merge the inputFile page and the temporary numbering page
        inputPage.merge_page(page)
        
        # Add the merged page to the final output writer
        mergeWriter.add_page(inputPage)

    # Delete the temporary file
    os.remove("tempNumbering.pdf")

    # Write the merged output
    with open(outputFile, 'wb') as fh:
        mergeWriter.write(fh)


#merge pdfs
merger = PyPDF2.PdfWriter()
for pdf in range(pdfn):
    merger.append(f"unmergedpdfs/{pdf+1}.pdf")

merger.write("Output.pdf")
merger.close()


