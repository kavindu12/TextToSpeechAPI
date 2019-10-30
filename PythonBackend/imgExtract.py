#! python

from __future__ import print_function

import fitz
from tkinter import *
import shutil
import os
from keras.preprocessing import image

import numpy as np
from keras.models import load_model

def ExImages(filepath):


    # print("This is my file "+filepath)
    checkXO = r"/Type(?= */XObject)"  # finds "/Type/XObject"
    checkIM = r"/Subtype(?= */Image)"  # finds "/Subtype/Image"


    # myfile = './pdfs/demo.pdf'      # file path
    stream = open(filepath, "rb").read()
    doc = fitz.open("pdf", stream)


    imgcount = 0
    lenXREF = doc._getXrefLength()  # number of objects - do not use entry 0!


    num = 1

    if os.path.isdir("../pdfImg"):
        shutil.rmtree('../pdfImg')

    os.mkdir('../pdfImg')

    for i in range(1,lenXREF):  # scan through all objects
            text = doc._getXrefString(i)  # string defining the object
            isXObject = re.search(checkXO, text)  # tests for XObject
            isImage = re.search(checkIM, text) # tests for Image
            if not isXObject or not isImage:  # not an image object if not both True
                continue
            imgcount += 1
            pix = fitz.Pixmap(doc, i)  # make pixmap from image
            if pix.n < 5: # can be saved as PNG
               pix.writePNG("../pdfImg/%s.png" % (num,))
               num+=1


            else:  # must convert the CMYK first
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG("../pdfImg/%s.png" % (num,))
                num+=1
                pix0 = None  # free Pixmap resources
                pix = None  # free Pixmap resources




    print("run time")
    print("extracted images", imgcount)

   #training model

    classifier = load_model("./Datafiles/classifier.model")
    classifier2 = load_model("./Datafiles/classifier2.model")
    classifier3 = load_model("./Datafiles/classifier3.model")

    results = []

    for pic in range(imgcount):
        path = '../pdfImg/' + str(pic+1) + '.png'
        test_image = image.load_img(path, target_size=(64, 64))
        test_image = np.expand_dims(test_image, axis=0)
        result = classifier.predict(test_image)
        result2 = classifier2.predict(test_image)
        result3 = classifier3.predict(test_image)


        if result[0][0] >= 0.5:

            if result2[0][0] >=0.5:
                st = "\nIMAGE : "
                stmt = ".png\nGRAPH CATEGORY : Linear Graph\nGRAPH SUB-CATEGORY : Negative Linear Graph\nGRAPH EQUATION : Y = -MX + C\nGRAPH EXPLANATION :Straight line graph that equation on 'm' is equal to the tangent of the angle that the line makes with the Negative direction of the X axis.\n"
                prediction = (st+str(pic+1)+stmt)
                results.append(prediction)

            else:
                st = "\nIMAGE : "
                stmt = ".png\nGRAPH CATEGORY : Linear Graph\nGRAPH SUB-CATEGORY : Positive Linear Graph\nGRAPH EQUATION : Y = MX + C\nGRAPH EXPLANATION :Straight line graph that equation on 'm' is equal to the tangent of the angle that the line makes with the Positive direction of the X axis.\n"
                prediction = (st + str(pic + 1) + stmt)
                results.append(prediction)

        else:
             if result3[0][0] >=0.5:
                 st = "\nIMAGE : "
                 stmt = ".png\nGRAPH CATEGORY : Curve Graph\nGRAPH SUB-CATEGORY : Graphs of Quadratic Equation-(OPENS DOWN Graph)\nGRAPH EQUATION : Y = aX^2 + bX + C\nGRAPH EXPLANATION :A symmetric graph,that the sign on the coefficient 'a' is less than zero.The maximum extreme point's gradient become zero.Start from the bottom and gradually increase.Reach to the extreme point from both sides.\n"
                 prediction = (st + str(pic + 1) + stmt)
                 results.append(prediction)

             else:

                 st = "\nIMAGE : "
                 stmt = ".png\nGRAPH CATEGORY : Curve Graph\nGRAPH SUB-CATEGORY : Graphs of Quadratic Equation-(OPENS UP Graph)\nGRAPH EQUATION : Y = aX^2 + bX + C\nGRAPH EXPLANATION :A symmetric graph,that the sign on the coefficient 'a' is grater than zero.The minimum extreme point's gradient become zero.Start from the top and gradually decrease.Reach to the extreme point from both sides.\n"
                 prediction = (st + str(pic + 1) + stmt)
                 results.append(prediction)

    separator = '\n'
    res_text = separator.join(results)
    print(res_text)
    return res_text



# root = ExImages()







