import cv2
import glob
import numpy as np
from xml.dom import minidom
import xml.etree.cElementTree as ET


folder_path = "C:\\MyLearnings\\openCV\\train\\Apple\\*.jpg"
xml_file_path = "C:\\MyLearnings\\openCV\\train\\Apple_xml\\"



filename_xml = ""
ht = -1
wd = -1
image = np.zeros((1,1,1),np.uint8)
saved_upimage = image
array = np.zeros((1,1,1),np.uint8)

X1 = -1
Y1 =-1
X1_save = -1
Y1_save = -1
X2_save = -1
Y2_save = -1

draw = False
save_clicked = False



def save_click():
    global ET, filename_xml
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(filename_xml, "w") as f:
        f.write(xmlstr)

def button(ht,wd):
    global array
    font = cv2.FONT_HERSHEY_SIMPLEX 
    array = np.zeros([int(ht/3), wd, 3], dtype=np.uint8)
    array[:,:int(wd/2)] = [0, 255, 255] #Orange left side
    array[:,int(wd/2):] = [0, 255, 0]   #Blue right side

    array = cv2.putText(array,"Reset",(int(wd/7),int(ht/5)),font,1,(255, 0, 0) ,2,cv2.LINE_AA)
    array = cv2.putText(array,"Save",(int(wd/2 + wd/7),int(ht/5)),font,1,(255, 0, 0) ,2,cv2.LINE_AA)

    
def drawrect(event,x,y,flags,param):
    global  draw,image,X1,Y1,saved_upimage,array,X1_save,Y1_save,X2_save,Y2_save
    if event == cv2.EVENT_LBUTTONDOWN:
        X1=x
        Y1=y
        draw = True
        if (0<x<wd/2) and (ht<y<(ht + ht/3)):
            print("clicked reset")
        elif(wd/2<=x<wd) and(ht <y<(ht + ht/3)):
            print("Save clicked")
            save_click()
            save_clicked = True
            

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw == True:
            print("2")
            image2 = saved_upimage.copy()
            cv2.rectangle(image2,(X1,Y1),(x,y),(0,255,0),3)
            image= image2
            print(image.shape)
            cv2.imshow("LabelImage App",np.concatenate((image, array),axis=0))

    elif event == cv2.EVENT_LBUTTONUP:
        draw = False
        image2 = saved_upimage.copy()
        cv2.rectangle(image2,(X1,Y1),(x,y),(0,255,0),3)
        image= image2
        cv2.imshow("LabelImage App",np.concatenate((image, array),axis=0))
        saved_upimage = image2
        X1_save = X1
        Y1_save = Y1
        X2_save = x
        Y2_save = y
        write_xml()



def write_xml():
   
    BndBox = ET.SubElement(root, "BndBox")

    ET.SubElement(BndBox, "X1", name="X_1").text = str(X1_save)
    ET.SubElement(BndBox, "Y1", name="Y_1").text = str(Y1_save)
    
    ET.SubElement(BndBox, "X2", name="X_2").text = str(X2_save)
    ET.SubElement(BndBox, "Y2", name="Y_2").text = str(Y2_save)



cv2.namedWindow('LabelImage App')
cv2.setMouseCallback("LabelImage App",drawrect)
root = ET.Element("root")
file_path = glob.glob(folder_path)
for image_path in file_path:
    image = cv2.imread(image_path)
    saved_upimage = image
    ht,wd,channels = image.shape
    filename_xml = xml_file_path+(image_path.rsplit('\\')[-1])
    filename_xml = filename_xml[:-3]
    filename_xml = filename_xml + "xml"
    button(ht,wd)
    cv2.imshow("LabelImage App",np.concatenate((image, array),axis=0))
    #while (save_clicked == False):
     #   pass
    cv2.waitKey(0)

cv2.destroyAllWindows()
