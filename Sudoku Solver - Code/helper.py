import cv2
import numpy as np
from tensorflow.keras.models import load_model
def initialiseModel():
    model=load_model('predModel.h5')
    return model

def process(img):
    grayImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresholdImg=cv2.adaptiveThreshold(grayImg,255,1,1,11,2)
    return thresholdImg


def points_clockwise_order(points):
    points=points.reshape((4,2))
    sq=np.zeros((4,1,2),dtype=np.int32)
    sum=points.sum(axis=1)
    sq[0]=points[np.argmin(sum)]
    sq[3]=points[np.argmax(sum)]
    diff=np.diff(points,axis=1)
    sq[1]=points[np.argmin(diff)]
    sq[2]=points[np.argmax(diff)]
    return sq

    
def biggestContour(contours):
    biggest=np.array([])
    max_area=0
    for ctr in contours:
        area=cv2.contourArea(ctr)
        if(area>50):
            ctrperi=cv2.arcLength(ctr,True)
            approx=cv2.approxPolyDP(ctr,2*ctrperi/100,True)
            if(area>max_area and len(approx)==4):
                biggest=approx
                max_area=area
    return biggest,max_area

def display(img,filled_cells,color=(0,255,0)):
    W=int(img.shape[1]/9)
    H=int(img.shape[0]/9)
    for x in range(0,9):
        for y in range(0,9):
            if(filled_cells[(y*9)+x]!=0):
                cv2.putText(img,str(filled_cells[(y*9+x)]),(x*W+int(W/2)-10,int((y+0.8)*H)),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,color,2,cv2.LINE_AA)
    return img



def predictCell(cells,model):
    ans=[]
    for cell in cells:
        img=np.asarray(cell)
        img=img[4:img.shape[0]-4,4:img.shape[1]-4]
        img=cv2.resize(img,(28,28))
        img=img/255
        img=img.reshape(1,28,28,1)
        
        prediction=model.predict(img)
        classIndex=np.argmax(prediction,axis=-1)
        probability=np.amax(prediction)

        if(probability>0.75):
            ans.append(classIndex[0])
        else:
            ans.append(0)
    return ans;
    


def find_cells(warped):
    rows=np.vsplit(warped,[70,140,210,280,350,420,490,560])
    cells=[]
    for r in rows:
        cols=np.hsplit(r,[70,140,210,280,350,420,490,560])
        for cell in cols:
            cells.append(cell)
    return cells

    
    
    
    
    