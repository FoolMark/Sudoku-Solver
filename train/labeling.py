import cv2
import os
import numpy as np

def label(root):
    FLAG = [0] * 10
    dirs = os.listdir(root)
    for dir in dirs:
        if('jpg') not in dir:
            continue
        if('_') in dir:
            label = dir.split('.')[0].split('_')[1]
            FLAG[int(label)] += 1
            continue
        path = os.path.join(root,dir)
        print(path)
        img = cv2.imread(path)
        cv2.imshow("label",img)
        x = cv2.waitKey(0)
        label = x - 48
        idx = dir.split('.')[0]
        new_name = f'{idx}_{label}.jpg'
        new_path = os.path.join(root,new_name)
        os.rename(path,new_path)
        print(new_path)
    print(FLAG)

def split(root):
    FLAG = [0] * 10
    dirs = os.listdir(root)
    TRAIN_SAMPLE = []
    TRAIN_LABEL = []
    TEST_SAMPLE = []
    TEST_LABEL = []
    for dir in dirs:
        if('_') in dir:
            label = int(dir.split('.')[0].split('_')[1])
            path = os.path.join(root,dir)
            img = cv2.imread(path)
            if FLAG[label] < 10:
                TEST_LABEL.append(label)
                TEST_SAMPLE.append(img[:,:,0]/255.)
            else:
                TRAIN_LABEL.append(label)
                TRAIN_SAMPLE.append(img[:,:,0]/255.)
            FLAG[label] += 1
    np.save('train_sample.npy',np.array(TRAIN_SAMPLE))
    np.save('train_label.npy',np.array(TRAIN_LABEL))
    np.save('test_sample.npy',np.array(TEST_SAMPLE))
    np.save('test_label.npy',np.array(TEST_LABEL))

if __name__ == '__main__':
    root = '../image/grid/'
    label(root)
    split(root)