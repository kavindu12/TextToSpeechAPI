from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
# c = canvas.Canvas('ex.pdf')
# c.drawString(3,3,"hello text")
# c.showPage()
# c.save()

#example 2

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter

# my_canvas = canvas.Canvas("txt_obj.pdf", pagesize=letter)
# textobject = my_canvas.beginText()

# # Set text location (x, y)
# textobject.setTextOrigin(cm*3, 730)

# # Set font face and size
# textobject.setFont('Times-Roman', 12)

# # Write a line of text + carriage return
# textobject.textLine(text='Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks! Python rocks!  ')

# # Change text color
# textobject.setFillColor(colors.red)

# # Write red text
# textobject.textLine(text='Python rocks in red!')

# # Write text to the canvas
# my_canvas.drawText(textobject)

# my_canvas.save()

#example 3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors

width, height = A4
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER

def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

# Texts

def addTextLine(c,text,x,y,unit,style):
    text_obj = Paragraph(text, style)
    text_obj.wrapOn(c, width-90, height)
    text_obj.drawOn(c, *coord(x, y, unit))

def generate_file(filename,generated_for_pdf,extracted_charts_pages):
        
    c = canvas.Canvas("./out/"+filename, pagesize=A4)
    row = 3

    tab_width=2.0
    line_height=0.5

    addTextLine(c,f'Generated from file:{generated_for_pdf}',1.8,2,cm,styleN)

    print('flow charts --------------------------------------')
    page_diagram_no = 1

    for flow_diagrms_page in extracted_charts_pages:
        diagrems,page_number = flow_diagrms_page
        if len(diagrems)<1:
            continue
        
        row+=line_height
        row+=line_height

       
        
        for flow_diagrm_dicition_score in diagrems:

            row = 3
            print(f'--------------------page_number:{page_number}------------------page_diagram_no:{page_diagram_no}')
       
            addTextLine(c,f"<strong>Flow diagram</strong>: {page_diagram_no}",1.8,row,cm,styleN)
            row+=line_height
            addTextLine(c,f"<strong>From Page No</strong>: {page_number}",1.8,row,cm,styleN)
            row+=line_height

            diagrem,dicition_score=flow_diagrm_dicition_score
            
            print(f"dicition_match_score:{dicition_score}")
            dicision_text= 'No'
            if dicition_score>0:
                dicision_text = "Yes"

            addTextLine(c,"<strong>Have Dicisions : </strong> "+dicision_text,1.8,row,cm,styleN)
            row +=line_height
            row +=line_height

            text_list = []
            for item in diagrem:
                itemx,itemy,itemw,itemh,text =item
                print([ itemx,itemy,itemw,itemh,text])
                text_list.append([text])
                # addTextLine(c,"<strong>*</strong> "+text,1.8+tab_width,row,cm,styleN)
                # row +=line_height

            table = Table(text_list)
            # table.setStyle(TableStyle([
            #     ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            #     ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            #     ('ALIGN',(0, 0),(0,-1), 'CENTER'),
            #     ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            #     ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            # ]))

            table.wrapOn(c, width-90, height)
            table.drawOn(c, 1.8*cm, 18.5*cm)

            page_diagram_no+=1
            c.showPage()

    c.save()

# descrpcion = Paragraph('<strong>*</strong> librart task.', styleN)
# descrpcion.wrapOn(c, width-90, height)
# descrpcion.drawOn(c, *coord(1.8, 3, cm))

# c.showPage()

# row = 0
# addTextLine(c,"Flow diagram: 01",1.8,3,cm,styleN)
# row+=1

