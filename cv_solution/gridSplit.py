import cv2
import os
import numpy as np

def getLines(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray,threshold1=50,threshold2=255,apertureSize=3)
    lines = cv2.HoughLines(edge,rho=1,theta=np.pi/180, threshold=169)
    h_lines,v_lines =clearLines(lines)
    #Plan I
    if len(h_lines) == 12 and len(v_lines) == 12:
        return h_lines,v_lines
    #Plan II
    else:
        h_first,h_last = h_lines[0],h_lines[-1]
        v_first,v_last = v_lines[0],v_lines[-1]
        w = 8
        y_diff = int((h_last[-2]+h_last[-1]-h_first[-2]-h_first[-1])/2-2*w)/9.
        x_diff = int((v_last[0]+v_last[1]-v_first[0]-v_first[1])/2-2*w)/9.
        X = []
        Y = []
        y_first,y_last = h_first[-1],h_last[-1]
        x_first,x_last = v_first[0],v_last[0]
        for i in range(10):
            if i==0:
                X.append(x_first)
                Y.append(y_first)
            else:
                X.append(int(X[-1]+x_diff))
                Y.append(int(Y[-1]+y_diff))
            if i in [3,6]:
                X.append(int(X[-1]+w))
                Y.append(int(Y[-1]+w))
        assert len(X) == 12 and len(Y) == 12
        h_lines = []
        v_lines = []
        for i in range(12):
            h_lines.append([X[0],X[-1],Y[i],Y[i]])
            v_lines.append([X[i],X[i],Y[0],Y[-1]])
        return h_lines,v_lines

def drawLines(img,lines):
    for l in lines:
        x1,x2,y1,y2 = l
        cv2.line(img,[x1,y1],[x2,y2],(0,0,255),2)
    cv2.imshow("Test",img)
    cv2.waitKey(0)

def displaySplit(img):
    h,v = getLines(img)
    drawLines(img,h+v)

def clearLines(lines):
    h = []
    v = []
    for line in lines:
        rho = line[0][0]
        theta = line[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = rho*a
        y0 = rho*b
        x1 = int(x0+1000*(-b))
        y1 = int(y0+1000*a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)
        if abs(x1-x2) > abs(y1-y2):
            h.append([x1,x2,y1,y2])
        else:
            v.append([x1,x2,y1,y2])
    h = sorted(h,key=lambda x:x[2])
    v = sorted(v,key=lambda x:x[0])
    h_lines = [h[0]]
    v_lines = [v[0]]
    for h_line in h:
        y = h_line[2]
        if abs(y-h_lines[-1][2])>=30:
            h_lines.append(h_line)
    for v_line in v:
        x = v_line[0]
        if abs(x-v_lines[-1][0])>=30:
            v_lines.append(v_line)
    if len(h_lines) == 10 and len(v_lines) == 10:
        ret_h = []
        ret_v = []
        for i in range(10):
            ret_h.append(h_lines[i])
            ret_v.append(v_lines[i])
            w = 8
            if i in [3,6]:
                ret_h.append([h_lines[i][0],h_lines[i][1],h_lines[i][2]+w,h_lines[i][3]+w])
                ret_v.append([v_lines[i][0]+w,v_lines[i][1]+w,v_lines[i][2],v_lines[i][3]])
        return ret_h,ret_v
    else:
        return h_lines,v_lines

def getGrids(img):
    h_lines,v_lines = getLines(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray,169,255,cv2.THRESH_BINARY)[1]
    grids = []
    for i in range(11):
        if i in[3,7]: continue
        h1,h2 = h_lines[i],h_lines[i+1]
        for j in range(11):
            if j in [3,7]: continue
            v1,v2 = v_lines[j],v_lines[j+1]
            x1,x2 = v1[0],v2[0]
            y1,y2 = h1[-1],h2[-1]
            grids.append(binary[y1:y2,x1:x2])
    return grids


def kNN(query,base,label,k=10):
    FLAG = [0] * 10
    score = np.dot(query,base.transpose())[0]
    idx = np.argsort(score)[::-1][:k]
    for i in idx:
        FLAG[label[i]] += 1
    return np.argmax(FLAG)

if __name__ == '__main__':
    img_path = 'input.jpg'
    img = cv2.imread(img_path)
    grids = getGrids(img)
    output = []
    for i in range(81):
        grid = grids[i][10:-10,10:-10]
        score = sum(sum(255. - grid))
        img = cv2.resize(grid,(48,48))
        output.append(img.reshape(-1,48*48)/255.)
    output = np.array(output)
    x,y =  np.load('cv_solution/train_sample.npy').reshape(-1,48*48),np.load('cv_solution/train_label.npy')
    x /= np.linalg.norm(x,axis=1,keepdims=True)
    labels = []
    for i in range(81):
        labels.append(kNN(output[i],x,y))
    np.save('input_label.npy',np.array(labels))

    





                