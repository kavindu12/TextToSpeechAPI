json_data_str="""
[[[], 1], [[[[[55, 20, 216, 73, "First, Black and white stripes is a little wide and low contrast"], [428, 20, 198, 72, "Adjust Black and white stripes contrast to low"], [55, 143, 216, 73, "Modify Black and white stripes contrast,"], [428, 143, 198, 56, "Next Frequency"], [84, 262, 197, 148, "user can see Black  and white stripes of  image or not"], [316, 277, 214, 119, "all frequency have  beed tesed"], [107, 291, 174, 90, "user can see Black  and white stripes"], [199, 352, 49, 29, "not"], [349, 462, 289, 56, "sensitivity perception inspection"], [43, 490, 404, 28, "Figure 4: Flowchart of the contrast sensitivity"]], 1], [[[216, 23, 139, 46, "Q start >"], [178, 106, 219, 87, "the output imag See"], [23, 206, 190, 37, "normal color vision"], [383, 206, 190, 41, "Color vision defects"], [23, 283, 190, 40, "color different measurement."], [383, 283, 190, 40, "Measurement of hue and saturation"], [207, 384, 172, 28, "C =>"]], 0], [[[500, 332, 181, 62, "method for color  color bar, (c) to"], [51, 342, 615, 128, "Figure    a blind. (a) original b be perceived color after hue transformation, (d) original c image, and (e) adjusted image."], [212, 342, 378, 77, "6: Example (a) original color bar, (b) perceived after hue transformation, (d)"], [314, 342, 352, 78, "of compensation color bar, (b) color bar, (c) to (d) original"]], 0], [[[108, 22, 118, 34, "Image"], [39, 85, 248, 115, "ered, green, and blue al ei yam"], [223, 165, 233, 103, "red-green or color blindness,"], [206, 215, 295, 165, "Speer pence nye color blindness Tot color \u2018olor space ation"], [411, 270, 167, 48, "Color space transform"], [129, 276, 160, 48, "Adjustment of color saturation"], [223, 432, 157, 26, "e_revised image"]], 0], [[[145, 20, 191, 42, "System Start"], [349, 88, 238, 55, "Vision and Vision surement for personal vipual model"], [145, 174, 191, 55, "Initialize video device then capture outside image"], [146, 248, 190, 57, "Adjust Image content by Personal visual mode"], [146, 328, 190, 42, "Output modify image"], [191, 436, 139, 18, "Is Suitable for user"], [43, 470, 89, 50, "System End"]], 3]], 2]]"""

template_html_file="template.html"

file_title="""<p>Generated from file:__PDFPATH__</p>"""
file_page_break="""<p style="page-break-before: always"></p>"""
digrem_content ="""
 <div style="margin-top: __MARGIN_TOP__px;">
      __PDFPATH_TEXT__
      <p><strong>Flow diagram:</strong> __PAGE_DIGRM_NO__</p>
      <p><strong>From Page:</strong> __PAGE_FROM_PAGE_NO__</p>
      <p><strong>Have Decisions:</strong> __PAGE_DICISIONSTATUS__</p>
      <p>Flow Chart:</p>
      <ul>
        __CONTENTLIST__
      </ul>
    </div>
    """



def addListItem(text):
   return f"<li>{text}</li>"
def generate_str(filename,generated_for_pdf,extracted_charts_pages):
    template_html='FlowChart Document\n'
   
    page_diagram_no = 1

    html_content=""

    digrem_contents_str=""

    for flow_diagrms_page in extracted_charts_pages:
        diagrems,page_number = flow_diagrms_page
        if len(diagrems)<1:
            continue
          
        
        for flow_diagrm_dicition_score in diagrems:

            row = 3
            
            digrem_template = ""

            if page_diagram_no==1 :
                digrem_template+="Generetad for: "+generated_for_pdf+"\n"
            else:
                digrem_template="\n\n"
            


            digrem_template+="Flow diagram: "+str(page_diagram_no)+"\n"
            digrem_template+="From Page: "+str(page_number)+"\n"

            diagrem,dicition_score=flow_diagrm_dicition_score
            
            dicision_text= 'No'
            if dicition_score>0:
                dicision_text = "Yes"
            
            digrem_template+="Have Dicisions: "+dicision_text+"\n"
            digrem_template+="Flow Chart: \n"
            
            listItems_str = ""
            for item in diagrem:
                itemx,itemy,itemw,itemh,text =item
                
                listItems_str+="\t"+text+"\n"
            digrem_template+=listItems_str

            page_diagram_no+=1
            digrem_contents_str+=digrem_template
   
    return digrem_contents_str

# def generate_file(filename,generated_for_pdf,extracted_charts_pages):
#     # import json

#     # extracted_charts_pages = json.loads(extracted_charts_pages)


#     template_html=''
#     with open(template_html_file, 'r') as file:
#         template_html = file.read().replace('\n', '')

   
#     page_diagram_no = 1
#     # if len(extracted_charts_pages)<1:
#     #     return

#     # first_page_data = extracted_charts_pages[0]
#     # diagrems,page_number = first_page_data
#     # if len(diagrems)<1:
#     #     return
#     # fp_content_str = ""+first_page_content


#     html_content=""+file_title
    

#     # fp_content_str=fp_content_str.replace("__PAGE_DIGRM_NO__",page_diagram_no)
#     # fp_content_str=fp_content_str.replace("__PAGE_FROM_PAGE_NO__",page_number)
#     # fp_content_str=fp_content_str.replace("__PAGE_DICISIONSTATUS__",generated_for_pdf)

#     # template_html=template_html.replace("__PAGE_CONTENTLIST__",fp_content_str)

  

#     digrem_contents_str=""

#     for flow_diagrms_page in extracted_charts_pages:
#         diagrems,page_number = flow_diagrms_page
#         if len(diagrems)<1:
#             continue
          
        
#         for flow_diagrm_dicition_score in diagrems:

#             row = 3
            
#             digrem_template = ""+digrem_content

#             if page_diagram_no==1 :
#                 digrem_template=digrem_template.replace("digrem_template","30")
#                 digrem_template=digrem_template.replace("__PDFPATH_TEXT__",generated_for_pdf)
#             else:
#                 digrem_template=digrem_template.replace("digrem_template","100")
#                 digrem_template=digrem_template.replace("__PDFPATH_TEXT__","")
#                 digrem_template=file_page_break+digrem_template
            
            

#             print(f'--------------------page_number:{page_number}------------------page_diagram_no:{page_diagram_no}')
#             digrem_template=digrem_template.replace("__PAGE_DIGRM_NO__",str(page_diagram_no))
#             digrem_template=digrem_template.replace("__PAGE_FROM_PAGE_NO__",str(page_number))

#             diagrem,dicition_score=flow_diagrm_dicition_score
            
#             print(f"dicition_match_score:{dicition_score}")
#             dicision_text= 'No'
#             if dicition_score>0:
#                 dicision_text = "Yes"
            
#             digrem_template=digrem_template.replace("__PAGE_DICISIONSTATUS__",dicision_text)


#             listItems_str = ""
#             for item in diagrem:
#                 itemx,itemy,itemw,itemh,text =item
#                 print([ itemx,itemy,itemw,itemh,text])
                
#                 listItems_str+=addListItem(text)
#             digrem_template=digrem_template.replace("__CONTENTLIST__",listItems_str)

#             page_diagram_no+=1
#             digrem_contents_str+=digrem_template
#     template_html=template_html.replace("__PAGE_CONTENTLIST__",digrem_contents_str)
#     with open("./out/"+filename, "w") as text_file:
#         text_file.write(template_html)

