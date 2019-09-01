import PyPDF2


def getPDFText(pdfFileObj):
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    noOfpages = pdfReader.getNumPages();
    index = 1;
    pdfText = "";
    while index < noOfpages:
        # print(index)
        pageObj = pdfReader.getPage(index);
        pdfText = pdfText + pageObj.extractText()
        index += 1;
    return pdfText;