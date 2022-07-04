
def valid(sudoku,num,x,y):
    for i in range(0,9):
        if(y!=i and sudoku[x][i]==num):
            return False
        elif(x!=i and sudoku[i][y]==num):
            return False
    
    box_x=x//3
    box_y=y//3
    for i in range(box_x*3,box_x*3+3):
        for j in range(box_y*3,box_y*3+3):
            if(sudoku[i][j]==num and (i,j)!=(x,y)):
                return False
    return True

def solve(sudoku,x,y):
    if(x==9):
        return True
    if(sudoku[x][y]!=0):
        if(valid(sudoku,sudoku[x][y],x,y)):
            if(y+1<9):
                return solve(sudoku,x,y+1)
            else:
                return solve(sudoku,x+1,0)
        else:
            return False
    else:
        ans=False
        for i in range(1,10):
            if(valid(sudoku,i,x,y)):
                sudoku[x][y]=i
                if(y+1<9):
                    ans=ans or solve(sudoku,x,y+1)
                else:
                    ans=ans or solve(sudoku,x+1,0)
                if(ans==True):
                    return ans
                sudoku[x][y]=0
        return ans
    

            