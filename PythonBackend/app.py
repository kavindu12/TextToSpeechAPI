from flask import Flask, jsonify,request
from convertPdfToString import getPDFText
import flowChartDetector


app = Flask(__name__)


@app.route("/pdf_flow_chart_response",methods=["GET"])
def jsonres():
    filename="./pdfs/"+request.args['filename']
    print(filename)
    genereted_str=flowChartDetector.process_pdf_file_to_flow_diagrm(filename)

    # return jsonify({'status':'success','datastr':genereted_str})
    return genereted_str

@app.route('/researchPaperText',methods=["GET"])
def hello_world():

    pdfFileObj = open('E:\SLIIT\PDF\demo.pdf','rb')     #'rb' for read binary mode
    allText =getPDFText(pdfFileObj)
    return jsonify({"text":allText})

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response




if __name__ == '__main__':
    app.run()
