import numpy as np

def load(train):
    if train == True:
        x,y =  np.load('train_sample.npy').reshape(-1,48*48),np.load('train_label.npy')
        x /= np.linalg.norm(x,axis=1,keepdims=True)
    else:
        x,y = np.load('test_sample.npy').reshape(-1,48*48),np.load('test_label.npy')
        x /= np.linalg.norm(x,axis=1,keepdims=True)
    return x,y

def kNN(query,base,label,k=10):
    FLAG = [0] * 10
    score = np.dot(query,base.transpose())
    idx = np.argsort(score)[::-1][:k]
    for i in idx:
        FLAG[label[i]] += 1
    return np.argmax(FLAG)


if __name__ == '__main__':
    x,y = load(train=True)
    X,Y = load(train=False)
    l = len(X)
    correct = 0
    for i in range(l):
        predict = kNN(X[i],x,y)
        if predict == Y[i]:
            correct += 1
    print('Test Acc:')        
    print(float(correct)/l * 100)
