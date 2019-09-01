from flask import Flask, jsonify
from convertPdfToString import getPDFText

app = Flask(__name__)


@app.route('/')
def hello_world():

    pdfFileObj = open('E:\SLIIT\PDF\demo.pdf','rb')     #'rb' for read binary mode
    allText =getPDFText(pdfFileObj)
    return jsonify({"about":allText})


if __name__ == '__main__':
    app.run()
