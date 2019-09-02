import cv2
import numpy as np

from os import listdir
from os.path import isfile, join

from pdf2image import convert_from_path

import base64
import matplotlib.pyplot as plt

import pytesseract
from pytesseract import Output

import myUtils
# import myPdfLib
import myHTMLLib



# pip3 install pytesseract
# C:\Program Files\Tesseract-OCR
# https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

config = ('-l eng --oem 1 --psm 4')

sxdelta =20
sydelta =20
extract_min_text_length=1

insiderdelta =10
min_text_recog_in_chart=10
font = cv2.FONT_HERSHEY_SIMPLEX

debugging_imshows=False

def imageToStr(img):
    retval, buffer = cv2.imencode('.jpg', img)
    b64_img_encoded_bytes = base64.b64encode(buffer)
    return b64_img_encoded_bytes.decode(ENCODING)

def ocr_text_to_list(strv):
    strlist =  strv.split('\n')
    filteredlistStrs= []
    for linestr in strlist:
        strv = linestr.strip()
        if len(strv)>0  :
            filteredlistStrs.append(strv)
        
    return  filteredlistStrs

def detect_convexHull(color_image_):
    image = cv2.cvtColor(color_image_,cv2.COLOR_BGR2HLS)
    lower = np.uint8([0, 200, 0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    # yellow color mask
    lower = np.uint8([10, 0,   100])
    upper = np.uint8([40, 255, 255])
    yellow_mask = cv2.inRange(image, lower, upper)
    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    result = color_image_.copy()

    
    if debugging_imshows==True:
        cv2.imshow("mask",white_mask) 

    height,width = mask.shape
    skel = np.zeros([height,width],dtype=np.uint8)      #[height,width,3]
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    temp_nonzero = np.count_nonzero(mask)

    num_rounds=0
   
    
    while(np.count_nonzero(mask) != 0 and num_rounds<1):
        eroded = cv2.erode(mask,kernel)

        if debugging_imshows==True:
            cv2.imshow("eroded",eroded)   
        temp = cv2.dilate(eroded,kernel)
        if debugging_imshows==True:
            cv2.imshow("dilate",temp)
        temp = cv2.subtract(mask,temp)
        skel = cv2.bitwise_or(skel,temp)
        mask = eroded.copy()
        num_rounds+=1
    return  cv2.erode(mask,kernel)


#find yes no matches and count score
def dicision_match_in_diagrm(color_input_img,diagram_n):
    img_height, img_width,_ = color_input_img.shape 
    min_w,min_h,max_w,max_h = 25,25,500,500
    bordersize =20

    base_size=img_height+bordersize*2,img_width+bordersize*2,3

    base=np.zeros(base_size,dtype=np.uint8)
    cv2.rectangle(base,(0,0),(img_width+bordersize*2,img_height+bordersize*2),(255,255,255),bordersize*2) # really thick white rectangle
    base[bordersize:img_height+bordersize,bordersize:img_width+bordersize]=color_input_img 

    gray_input = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    
    d = pytesseract.image_to_data(gray_input, output_type=Output.DICT, config=config)
    # -------------------------------------------------
    # if debugging_imshows==True:
    #     n_boxes = len(d['level'])
    #     print("text bound")
    #     print(d)
    #     print(n_boxes)
    #     for i in range(n_boxes):
    #         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    #         cv2.rectangle(color_input_img_new, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
    #     if debugging_imshows==True:
    #         cv2.imshow(f"text collected_items_yes_no_dicition{diagram_n}",color_input_img_new)  
    # -------------------------------------------------
    n_boxes_texts = len(d['text'])

    # dicision match list
    dicition_matches = ["yes","no"]
    dicition_match_score=0
    for i in range(n_boxes_texts):
        text_d =d['text'][i].strip().lower()
        if len(text_d) >0 and any(text_d in s_text for s_text in dicition_matches):
            dicition_match_score+=1
    
    return dicition_match_score



def extract_text_string(color_input_img):
    gray_input = cv2.cvtColor(color_input_img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_input, config=config)
    if len(text)>extract_min_text_length :
        extracted_listdata = ocr_text_to_list(text)
        if(len(extracted_listdata)>0) :
            return extracted_listdata
    return None

#green box, text detect, text near by box create
def detect_text_box(color_input_img,diagram_n):
    img_height, img_width,_ = color_input_img.shape 
  
    bordersize =20

    base_size=img_height+bordersize*2,img_width+bordersize*2,3

    base=np.zeros(base_size,dtype=np.uint8)
    cv2.rectangle(base,(0,0),(img_width+bordersize*2,img_height+bordersize*2),(255,255,255),bordersize*2) 
    base[bordersize:img_height+bordersize,bordersize:img_width+bordersize]=color_input_img 

    color_input_img_new=base    

    gray_input = cv2.cvtColor(color_input_img_new, cv2.COLOR_BGR2GRAY)    

    d = pytesseract.image_to_data(gray_input, output_type=Output.DICT, config=config)

    n_boxes = len(d['level'])
    
    collected_list = []
    sydelta =5
    sxdelta =5

    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        area = w * h
        similler_found=False
        if w> (img_width*40/100) or h > (img_height*40/100):
            continue
        # remove simillar box (ex:Non max supression)
        for crect in collected_list:
            cx,cy,cw,ch ,text= crect
            if abs(x-cx)< sxdelta and abs(y-cy) < sydelta and abs(w-cw)<sxdelta and abs(h-ch)<sydelta:
                similler_found = True
                break
                    
        if similler_found==False:
            collected_list.append([x,y,w,h,d['text'][i]]) 
    
    box_iv=0 
    
    for item_rect in collected_list:
        itemx,itemy,itemw,itemh ,text= item_rect
        cv2.rectangle(color_input_img_new,(itemx,itemy),(itemx+itemw,itemy+itemh),(0,255,0),2)
        cv2.putText(color_input_img_new,f"{text}",(itemx,itemy),font,0.5,(255,0,0),1,2)
        cv2.putText(color_input_img_new,f"{box_iv}",(itemx,itemy),font,0.5,(255,0,0),1,2)
        box_iv+=1
    box_iv=0
    
    kn_x = min(int(img_width/15),60)
    kn_y = min(int(img_height/24),25)

    print(f"knx:${kn_x}, kny:${kn_y}")
    col_dict_list = []
    for item_rect in collected_list:
        itemx,itemy,itemw,itemh,text = item_rect
       
        box_ik=0
        for item_rectk in collected_list:
            if box_iv != box_ik:
                kx,ky,kw,kh,text = item_rectk
                dxk = abs(kx-itemx-itemw)
                dyk = abs(ky-itemy-itemh)
                               
                if dxk <=kn_x and dyk <= kn_y:
                    
                    if len(col_dict_list)==0:
                        col_dict_list.append([box_iv,box_ik])
                    else:
                        found_in_group=False
                        for group in col_dict_list:
                            if box_iv in group  :

                                if box_ik not in group:
                                    group.append(box_ik)
                                found_in_group = True    
                                break

                        if found_in_group ==False:
                            for group in col_dict_list:
                                if box_ik in group :
                                        if box_iv not in group:
                                            group.append(box_iv)
                                        found_in_group = True
                                        break

                        if found_in_group ==False:
                            col_dict_list.append([box_iv,box_ik])

            box_ik+=1
        box_iv+=1


    #visualizing with bondry boxes for collected groups
    klist_collected= []
    padding_x=5
    padding_y=4
    string_data_list=[]
    for group in col_dict_list:
      
        kitem_0  = collected_list[group[0]]
        kitem_x=kitem_0[0]
        kitem_y=kitem_0[1]
        kitem_w=kitem_0[2]
        kitem_h=kitem_0[3]

        far_x=kitem_x
        far_y=kitem_y

        group.sort()
        # print(group)
        str_items=[]
        for k_i in group:
            kitem_i  = collected_list[k_i]
            str_items.append([kitem_i[0],kitem_i[1],kitem_i[2],kitem_i[3],kitem_i[4]])
            


            if kitem_x>kitem_i[0]:
                kitem_x = kitem_i[0]
            if kitem_y>kitem_i[1]:
                kitem_y = kitem_i[1]

            if far_x<kitem_i[0]+kitem_i[2]:
                far_x = kitem_i[0]+kitem_i[2]

            if far_y<kitem_i[1]+kitem_i[3]:
                far_y = kitem_i[1]+kitem_i[3]
        group_dim =[kitem_x-padding_x,kitem_y-padding_y,far_x-kitem_x+padding_x*2,far_y-kitem_y+padding_y*2]
        string_data_list.append([str_items,group_dim])
        klist_collected.append(group_dim)
    
    # print(string_data_list)
    red_str_data_list=[]
    for item_group in string_data_list:

        str1=""
        str_list,group_dim = item_group
        gpx,gpy,gpw,gph=group_dim
        # print(group_dim)
        for item_rect in str_list:
            itemx,itemy,itemw,itemh,text = item_rect
            str1+=text+" "
        # print(str1)
        red_str_data_list.append([gpx,gpy,gpw,gph,str1])

    # print(f"count::{len(collected_list)}")

    green_str_data_list=[]
    for item_rect in collected_list:
        itemx,itemy,itemw,itemh ,text= item_rect

        in_red_box=False
        for item_group in string_data_list:
            str_list,group_dim = item_group
            if itemx>group_dim[0] and itemx <group_dim[0] + group_dim[2] and itemy>group_dim[1] and itemy <group_dim[1] + group_dim[3]   :

                in_red_box=True
                break

        if in_red_box==False:
            green_str_data_list.append([itemx,itemy,itemw,itemh ,text])
    

    #we have red,green lists with locations and texts  red_str_data_list,green_str_data_list

    for item_rect in klist_collected:
        itemx,itemy,itemw,itemh = item_rect
        cv2.rectangle(color_input_img_new,(itemx,itemy),(itemx+itemw,itemy+itemh),(0,0,255),2)

       
        # cv2.putText(color_input_img_new,f"{box_iv}",(itemx,itemy),font,0.5,(255,0,0),1,2)
    if debugging_imshows==True:
        cv2.imshow(f"diagrm text boxes:{diagram_n}",color_input_img_new)  
  
    return green_str_data_list,red_str_data_list


#diagrem to box detect 
def diagram_item_detect(color_input_img,diagram_n):
    
    dicition_match_score=dicision_match_in_diagrm(color_input_img,diagram_n)
       
    img_height, img_width,_ = color_input_img.shape 
    min_w,min_h,max_w,max_h = 25,25,500,500
    bordersize =20
    # gray_input =  cv2.copyMakeBorder( gray_input, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,borderType= cv2.BORDER_CONSTANT,value = [255, 255, 0])

    base_size=img_height+bordersize*2,img_width+bordersize*2,3

    base=np.zeros(base_size,dtype=np.uint8)
    cv2.rectangle(base,(0,0),(img_width+bordersize*2,img_height+bordersize*2),(255,255,255),bordersize*2) # really thick white rectangle
    base[bordersize:img_height+bordersize,bordersize:img_width+bordersize]=color_input_img 

    color_input_img=base.copy()
    color_input_img2 = base.copy()
    

    gray_input = cv2.cvtColor(color_input_img, cv2.COLOR_BGR2GRAY)
    
    # ret,thresh_img = cv2.threshold(gray_input, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    # morph_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)
    # #prod cv2.imshow(f"morph_img",morph_img)  
    # gray_input = cv2.bilateralFilter(morph_img, 11, 17, 17)
    # kernel = np.ones((4,4),np.uint8)
    # erosion = cv2.erode(gray_input,kernel,iterations = 2)
    # kernel = np.ones((4,4),np.uint8)
    # dilation = cv2.dilate(erosion,kernel,iterations = 2)

    # edges = cv2.Canny(gray_input, 200, 200)
    # lines = cv2.HoughLinesP(gray_input, 1, 3.17/180, 50, minLineLength=50, maxLineGap=10)[0]
    
    # contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    ret, thresh = cv2.threshold(gray_input, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # ret, thresh = cv2.threshold(gray_input, 127, 255,0)
    # contours,hierarchy = cv2.findContours(thresh,2,1)

    # image_to_countr =detect_convexHull(color_input_img)
    # ret, thresh = cv2.threshold(image_to_countr, 127, 255,0)
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))

    rects = [cv2.boundingRect(cnt) for cnt in contours]
    rects = sorted(rects,key=lambda  x:x[1],reverse=True)

    i = -1
    j = 1
    y_old = 5000
    x_old = 5000
    collected_list = []
    sydelta =5
    sxdelta =5

    for rect in rects:
        x,y,w,h = rect
        area = w * h
        
        #remove smaller and too larger box
        if area > 250 and area < 700000  and w>min_w and w< max_w and h > min_h and h < max_h:

            similler_found=False
            # remove simillar box (Non-max supression)
            for crect in collected_list:
                cx,cy,cw,ch = crect
                case1 = abs(x-cx)< sxdelta and abs(y-cy) < sydelta and abs(w-cw)<sxdelta and abs(h-ch)<sydelta
                case2 = x<cx and y<cy and x+w>cx+cw and y+h>cy+ch
                case3 = x>cx and y>cy and x+w<cx+cw and y+h<cy+ch

                if case1 or case2 or case3:
                    similler_found = True
                    break
                        
            if similler_found==False:
                collected_list.append([x,y,w,h])

    blue_str_data_list=[]
    texti=0
    for item_rect in collected_list:
        itemx,itemy,itemw,itemh = item_rect
        if debugging_imshows==True:
            cv2.imshow(f"input_{diagram_n}{texti}",color_input_img[itemy:itemy+itemh, itemx:itemx+itemw]) 
        texti+=1
        text=extract_text_string( color_input_img[itemy:itemy+itemh, itemx:itemx+itemw])
        print(text)
        if text!=None and len(text)>0:
            text = " ".join(text)
            blue_str_data_list.append([ itemx,itemy,itemw,itemh,text])

        cv2.rectangle(color_input_img,(itemx,itemy),(itemx+itemw,itemy+itemh),(255,0,0),2)
        cv2.rectangle(color_input_img2,(itemx,itemy),(itemx+itemw,itemy+itemh),(255,255,255),-1)

    if debugging_imshows==True:
        cv2.imshow(f"input_{diagram_n}",color_input_img)  
        cv2.imshow(f"collected_items_{diagram_n}",gray_input)  
    
    # key = cv2.waitKey(100000)
    # if key == 27:
    #     cv2.destroyAllWindows()
    # exit(0)
    green_str_data_list,red_str_data_list = detect_text_box(color_input_img2,diagram_n)
    
    # print("00000000000000000000000000000000000000000")
    # print(len(blue_str_data_list))
    # print(len(green_str_data_list))
    # print(len(red_str_data_list))
    

    marged_str_data_list = []
    for item in blue_str_data_list:
        marged_str_data_list.append(item)

    for item in green_str_data_list:
        marged_str_data_list.append(item)

    for item in red_str_data_list:
        marged_str_data_list.append(item)

    marged_str_data_list_sorted =  sorted(marged_str_data_list, key=lambda x: x[1], reverse=False)
    items_count = len(marged_str_data_list_sorted)
    for idx in range(items_count-1):
        itemx,itemy,itemw,itemh,text = marged_str_data_list_sorted[idx]
        itemx2,itemy2,itemw2,itemh2,text2 = marged_str_data_list_sorted[idx+1]
        
        if itemx>itemx2 and itemy>=itemy2:
            marged_str_data_list_sorted[idx+1],marged_str_data_list_sorted[idx]= \
                                        marged_str_data_list_sorted[idx],marged_str_data_list_sorted[idx+1]

    print("===================================================")
    print("Result:")
    print(f"dicition_match_score:{dicition_match_score}")

    filtered_marged_str_data_list_sorted=[]
    for i in range(len(marged_str_data_list_sorted)):
        itemx,itemy,itemw,itemh,text =marged_str_data_list_sorted[i]
        text = text.strip()
        text = text.strip()
        if len(text)>0:
            filtered_marged_str_data_list_sorted.append([ itemx,itemy,itemw,itemh,text])
            print([ itemx,itemy,itemw,itemh,text])
    

    # text = pytesseract.image_to_string(gray_input, config=config)
    # print(text)
    # print(len(text))
    # if len(text)>10 :
    #     print("chart found:")
    #     extracted_listdata = ocr_text_to_list(text)
    #     if(len(extracted_listdata)>0) :
    #         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),5)
    #         print(extracted_listdata)

    return [filtered_marged_str_data_list_sorted,dicition_match_score]


def image_process(processing_image,min_area_pres=20,is_path=True,page_number=1):
   
    if is_path:
        img = cv2.imread(images_path+processing_image)
        # print(processing_image)
    else:
        img = processing_image

    img_height, img_width,_ = img.shape
    # print(img_width,img_height)

    min_w=int(img_width/50)
    max_w=int((img_width*60)/100)
    min_h=int(img_height/50)
    max_h=int((img_height*60)/100)
    
    min_area=(img_width*img_width*min_area_pres)/100 
    # print(f"min_area:{min_area}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(gray,kernel,iterations = 2)
    kernel = np.ones((4,4),np.uint8)
    dilation = cv2.dilate(erosion,kernel,iterations = 2)


    # kernal = np.ones ((15,15),np.float32)/255
    # smootheed = cv2.filter2D(gray,-1,kernal)

    # blur = cv2.GaussianBlur(gray,(5,5),0)
    # median = cv2.medianBlur(gray,15)
    # laplacian = cv2.Laplacian(gray,cv2.CV_64F)
    edged = cv2.Canny(dilation, 200, 200)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rects = [cv2.boundingRect(cnt) for cnt in contours]
    rects = sorted(rects,key=lambda  x:x[1],reverse=True)

    i = -1
    j = 1
    y_old = 5000
    x_old = 5000
    collected_list = []

    for rect in rects:
        x,y,w,h = rect
        area = w * h
        
        #remove smaller and too larger box
        if area > 1000 and area < 700000  and w>min_w and w< max_w and h > min_h and h < max_h:

            similler_found=False
            #remove simillar box
            for crect in collected_list:
                cx,cy,cw,ch = crect
                if abs(x-cx)< sxdelta and abs(y-cy) < sydelta and abs(w-cw)<sxdelta and abs(h-ch)<sydelta:
                    similler_found = True
                    break
                        
            if similler_found==False:
                collected_list.append([x,y,w,h])
    #remove inside boxs
    iterate= 0
    max_itr=len(collected_list)
    while iterate <max_itr:

        for crect in collected_list:
            x,y,w,h = crect
            for crect2 in collected_list:
                cx,cy,cw,ch = crect2
                if( x-insiderdelta < cx and y-insiderdelta < cy and x+w>cx+cw and y+h > cy+ch):
                    collected_list.remove(crect2)
        iterate += 1
    #remove smaller boxes
    filtered_list = []
    for crect in collected_list:
        cx,cy,cw,ch = crect
        # print(cw*ch)
        if cw*ch >min_area :
            filtered_list.append(crect)      
    #draw rectangles   
    diagram_n= 0

    extracted_charts=[]
    
    for crect in filtered_list:
        x,y,w,h = crect
                
        # if diagram_n!=5:
        #     diagram_n+=1
        #     continue
        cropped_image =  img[y:y+h, x:x+w]
        
        marged_str_data_list_sorted=diagram_item_detect(cropped_image,diagram_n)
        items_list,dicition_score=marged_str_data_list_sorted
        if len(items_list)>2:

            extracted_charts.append(marged_str_data_list_sorted)
            diagram_n+=1
        # min_text_recog_in_chart

   
    return extracted_charts




def process_pdf_file_to_flow_diagrm(pdf_file_path):

    # pages = convert_from_path(pdfs_paths[1],poppler_path="./poppler-0.68.0/bin")
    pages = convert_from_path(pdf_file_path,poppler_path="./poppler-0.68.0/bin")

    gen_str=myUtils.dictionaryRandom()
    gen_filename=gen_str+".pdf"
    gen_filename_html=gen_str+".html"
    print(gen_filename)
    
    page_number=1
    extracted_charts_pages=[]
    for page in pages:
        page = page
        

        # if page_number !=4:
        #     page_number+=1
        #     continue
        img = np.array(page)  #PIL image to numpy array
        extracted_charts=image_process(img,6,False,page_number)

        extracted_charts_pages.append([extracted_charts,page_number])

        page_number+=1
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()

    
    # import simplejson, json
    # x = simplejson.dumps(extracted_charts_pages)
    # print(x)
    # exit(0)
    # myPdfLib.generate_file(gen_filename,pdf_file_path,extracted_charts_pages)
    # myHTMLLib.generate_file(gen_filename_html,pdf_file_path,extracted_charts_pages)
    generetad_str=myHTMLLib.generate_str(gen_filename_html,pdf_file_path,extracted_charts_pages)
    print("------------------------------------")
    print(generetad_str)
    return generetad_str
   
      


# process_pdf_file_to_flow_diagrm('./pdfs/3.pdf')