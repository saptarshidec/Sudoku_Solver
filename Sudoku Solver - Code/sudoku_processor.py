import cv2
import numpy as np
from helper import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import sudoku_solve
from sys import exit

def main(image_path):
    img=cv2.imread(image_path)
    
    width=630
    height=630
    model=initialiseModel()

    blankimg=np.zeros((height,width,3),np.uint8)
    
    img=cv2.resize(img,(width,height))
    img_threshold=process(img)
    
    imgContours=img.copy()
    imgBigContour=img.copy()
    
    
    contours,hierarchy=cv2.findContours(img_threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours,contours,-1,(0,255,0),3)
    
    biggest,maxArea=biggestContour(contours)
    
    if(biggest.size!=0):
        biggest=points_clockwise_order(biggest)
        cv2.drawContours(imgBigContour,biggest,-1,(0,0,255),25)
        src=np.float32(biggest)
        dest=np.float32([[0,0],[width,0],[0,height],[width,height]])
        transform=cv2.getPerspectiveTransform(src,dest)
        warped=cv2.warpPerspective(img,transform,(width,height))
        
        imgwarped=cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
        contours,hierarchy=cv2.findContours(imgwarped,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        warpcopy=warped.copy()
        cv2.drawContours(warpcopy,contours,-1,(0,0,255),5)
        
        
        detected_digits=blankimg.copy()
        cells=find_cells(imgwarped)
        print(len(cells))
        if(len(cells)!=81):
            print("Sudoku grid not detected")
            return False
        filled_cells=predictCell(cells,model)
        
        filled_digits=display(detected_digits,filled_cells,color=(255,0,255))
        filled_cells=np.asarray(filled_cells)

        sudoku=np.array_split(filled_cells,9)
        
        for i in range(0,9):
            for j in range(0,9):
                if(sudoku[i][j]>=1 and sudoku[i][j]<=9):
                    print(sudoku[i][j],end=' ')
                else:
                    print('_',end=' ')
            print()
    
        ch='Y'
        print("Do you want to change any digit? Y/N",end=' ')
        ch=input()
        while(ch=='Y' or ch=='y'):
            print ("Enter row x column number:",end=' ')
            inp=input()
            r=(int)(inp[0])
            c=(int)(inp[2])
            print("Enter the value",end=' ')
            val=(int)(input())
            if(r-1>=0 and r-1<9 and c-1>=0 and c-1<9 and val>=1 and val<=9):
                sudoku[r-1][c-1]=val
                filled_cells[(r-1)*9+(c-1)]=val
            else:
                print("Wrong input")
            print("Do you want to change any digit? Y/N",end=' ')
            ch=input()
    
   
        avble_cells=np.where(filled_cells==0,1,0)
        res=sudoku_solve.solve(sudoku,0,0)
        if(res==False):
            print("Could not solve")
            return False
        
        
        flatGrid=[]
        for row in sudoku:
            for cell in row:
                flatGrid.append(cell)
        solvedcells=flatGrid*avble_cells
        img_solvedcells=blankimg.copy()
        img_solvedcells=display(img_solvedcells,solvedcells)
        
        
        dest=np.float32(biggest)
        src=np.float32([[0,0],[width,0],[0,height],[width,height]])
        inv_transform=cv2.getPerspectiveTransform(src,dest)
        imgInvWarped=img.copy()
        imgInvWarped=cv2.warpPerspective(img_solvedcells,inv_transform,(width,height))
        inv_perspective=cv2.addWeighted(imgInvWarped,1,img,0.5,1)
        path=os.path.splitext(image_path)
        status=cv2.imwrite('static/uploads/'+path[0]+'_output'+path[1],inv_perspective)
        
    else:
        print("Sudoku grid not detected")










