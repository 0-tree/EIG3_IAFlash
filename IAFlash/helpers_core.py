
import os
from PIL import Image

import matplotlib.pyplot as plt
from matplotlib import cm


#%%

def pcaPlot(X3,col,title=''):
    '''
    To be cleaned
    
    '''
    f = plt.figure(figsize=(18,6))
    
    ax = f.add_subplot(1,3,1)
    ax.scatter(X3[:,0],X3[:,1],color=col)
    ax.set_xlabel(0, fontsize = 15)
    ax.set_ylabel(1, fontsize = 15)
    ax.set_title(title)
    
    ax = f.add_subplot(1,3,2)
    ax.scatter(X3[:,0],X3[:,2],color=col)
    ax.set_xlabel(0, fontsize = 15)
    ax.set_ylabel(2, fontsize = 15)
#     ax.set_xlim(-4,8)
#     ax.set_ylim(-2,2)

    ax = f.add_subplot(1,3,3)
    ax.scatter(X3[:,1],X3[:,2],color=col)
    ax.set_xlabel(1, fontsize = 15)
    ax.set_ylabel(2, fontsize = 15)
#     ax.set_xlim(-4,8)
#     ax.set_ylim(-2,2)

    plt.show()



#%%

class OneClassPerDirImageHandler:
    
    def __init__(self, pathToDataDir):
        '''
        Inputs
        ------
        pathToDataDir : str
            path to the directory containing one directory per class
            and all images in each one of these subsirectories.
        '''

        self.pathToDataDir = pathToDataDir
                
        for _p in (self.pathToDataDir,):
            if not os.path.isdir(_p):
                raise ValueError('directory does not exist: {}'.format(_p))
        
        self.classDict = {}
        self.classDictInv = {}
        self.nbPerClass = {}
        self.filesPerClass = {}
        i = -1
        for root,folders,files in os.walk(self.pathToDataDir): # NB: this is walked in random order
            if folders == []:
                i += 1
                folder = os.path.split(root)[-1]
                self.classDict[i] = folder
                self.classDictInv[folder] = i
                self.nbPerClass[i] = len(files)
                self.filesPerClass[i] = files


    def getImage(self, classId, numId):
        '''
        returns the `numId` image for class `classId`.

        Inputs
        ------
        classId : int or str
            if int, index of the class as in classDict;
            if str, name of the self.classDictInv
        numId : int, list of int, or 'all'
            if int, index of the image in its class. Should be lower than self.nbPerClass[classId].
            if 'all', will return all images for that class.
        '''

        if isinstance(classId, int):
            classIdx_ = classId
            className_ = self.classDict[classId]
        elif isinstance(classId, str):
            classIdx_ = self.classDictInv[classId]
            className_ = classId
        else:
            raise TypeError('unkown type for classId: {}'.format(type(classId)))

        nbInClass = self.nbPerClass[classIdx_] 

        if isinstance(numId, int):
            numId_ = [numId]
        elif isinstance(numId, list):
            numId_ = numId
        elif 'all' == numId:
            numId_ = [i for i in range(nbInClass)]
        else:
            raise ValueError('numId not understood: {}'.format(numId))

        ls_im = []
        for n in numId_:
            if n > nbInClass:
                raise ValueError('numId ({}) larger than number of elements ({}) in class {}'.format(n,nbInClass,className_))
            path = os.path.join(self.pathToDataDir, className_, self.filesPerClass[classIdx_][n])
            im = Image.open(path)

            ls_im.append(im)

        if 1 == len(ls_im): # compatibility with numId == int
            ls_im = ls_im[0]

        return(ls_im)
     
#%%
                