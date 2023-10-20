from django.shortcuts import render
from django.http import HttpResponse
import PyPDF2,os,img2pdf
from PIL import Image
from django.conf import settings
from pdfManager.form import UploadFileForm
# Create your views here.

def home(request):
    return render(request,'home.html')

# Combine Two or more pdf into one single pdf 
def combineTwopdf(request):
    if request.POST and request.FILES:
        pdf = request.FILES['pdf']
        pdf2 = request.FILES['pdf2']
    
        pdfReader = PyPDF2.PdfReader(pdf)
        pdfReader2 = PyPDF2.PdfReader(pdf2)
        
        # creating a page object
        pageObj = pdfReader.pages[0]
        pageObj2 = pdfReader2.pages[0]

        list=[]
        list.append(pdf)
        list.append(pdf2)

        output = 'combined.pdf'
 
        # calling pdf merge function
        PDFmerge(pdfs=list, output=output)
 
        # extracting text from page
        print(pageObj.extract_text())

        pdf.close()
        pdf2.close()
        path = output+".pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, path)
      
        with open(output, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return HttpResponse("Pdf Merged Successfully")



#  Extract all text from pdf file to TXT file 
def extractall(request):
    if request.POST and request.FILES:
        pdfFileObj = request.FILES['pdf']
        print(pdfFileObj)
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
 
        # printing number of pages in pdf file
        print(len(pdfReader.pages))

        # creating a page object
        pageObj = pdfReader.pages[0]

        # extracting text from page
        print(pageObj.extract_text())

        output ="demofile3.txt"
        f = open(output, "w")
        f.write(pageObj.extract_text())
        f.close()

        path = output
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        with open(output, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
        # closing the pdf file object
        pdfFileObj.close()

    return HttpResponse("No File Found")



# Convert images into pdf JPG,TIFF and PNG
def convert(request):
    if request.POST and request.FILES:
        pdf = request.FILES['pdf']

        # converting into chunks using img2pdf
        pdf_bytes = img2pdf.convert(pdf)
        print(pdf)

        image="image.pdf"
        # Opening Pdf File 
        file = open(image, "wb")

        # writing pdf files with chunks
        file.write(pdf_bytes)

        # closing image file
        pdf.close()
 
        # closing pdf file
        file.close()

        path = image
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        with open(image, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    return HttpResponse("Images Appended in the pdf")



# Remove pdf Password for reading and editing
def removepdf(request):
    if request.POST and request.FILES:
        pdf = request.FILES['pdf']
        print(pdf)
    return HttpResponse("Remove password page")

    

# Separate PDF pages
def separatePdf(request):
    if request.POST and request.FILES:
        pdf = request.FILES['pdf']
        splits = [1,2]
        
 
    # calling PDFsplit function to split pdf
        PDFsplit(pdf, splits)
        

    return HttpResponse("Separate pdf")


def PDFsplit(pdf, splits):
  # creating input pdf file object
    
    file_name=pdf.name
 
    # creating pdf reader object
    pdfReader = PyPDF2.PdfReader(pdf)
 
    # starting index of first slice
    start = 0
 
    # starting index of last slice
    end = splits[0]
 
 
    for i in range(2):
        # creating pdf writer object for (i+1)th split
        pdfWriter = PyPDF2.PdfWriter()
 
        # output pdf file name
        outputpdf = file_name.split('.pdf')[0] + str(i) + '.pdf'
 
        # adding pages to pdf writer object
        for page in range(start,end):
            pdfWriter.add_page(pdfReader.pages[page])
 
            # writing split pdf pages to pdf file
            with open(outputpdf, "wb") as f:
                pdfWriter.write(f)
 
            # interchanging page split start position for next split
            start = end
            try:
                # setting split end position for next split
                end = splits[i+1]
            except IndexError:
                # setting split end position for last split
                end = len(pdfReader.pages)
 
    # closing the input pdf file object
    pdf.close()


def PDFmerge(pdfs, output):
    # creating pdf file merger object
    pdfMerger = PyPDF2.PdfMerger()
 
    # creating pdf file and then appending pdfs one by one
    for pdf in pdfs:
        pdfMerger.append(pdf)
 
        # writing combined pdf to output pdf file
        with open(output, 'wb') as f:
            pdfMerger.write(f)


