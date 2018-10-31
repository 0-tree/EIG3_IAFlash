

import os
import re
from PIL import Image
import xml.etree.ElementTree
import scipy.io # used to import .mat files with scipy.io.loadmat (see [here](https://stackoverflow.com/questions/874461/read-mat-files-in-python))




#%%

class DataHandler:
    
    def __init__(self, pathToDataDir):
        '''
        Inputs
        ------
        pathToDataDir : str
            path to the directory containing Images/ Annotations/ Lists/ etc.

        Notes
        -----
        - this class assumes no change is made in the structure of the
          downloaded directory
        '''

        self.pathToDataDir = pathToDataDir   
        self.pathToDataPatchDir = os.path.join(pathToDataDir, 'Patches') 
        # str : directory where patches are saved
        
        for _p in (self.pathToDataDir,):
            if not os.path.isdir(_p):
                raise ValueError('directory does not exist: {}'.format(_p))

        self._loadAnnos()
        self.n = len(self._cars_annos_files)
        

    def _loadAnnos(self):
        '''
        '''
        cars_annos = scipy.io.loadmat(self.pathToDataDir+'cars_annos.mat')

        self._cars_annos_bbox = [(int(x[1][0,0]),
                                  int(x[2][0,0]),
                                  int(x[3][0,0]),
                                  int(x[4][0,0])) for x in cars_annos['annotations'][0,:]]
        self._cars_annos_files = [x[0][0] for x in cars_annos['annotations'][0,:]]
        self._cars_annos_labels = [x[5][0,0]-1 for x in cars_annos['annotations'][0,:]] # NB: change to 0-based index
        self._cars_annos_isTest = [1 == x[6][0,0] for x in cars_annos['annotations'][0,:]]
        self._cars_annos_classnames = [x[0] for x in cars_annos['class_names'][0,:]]
            
    
    
#%%
                
class ImageWorker:
    
    def __init__(self, dataHandler, index):
        '''
        Inputs
        ------
        dataHandler : DataHandler
            DataHandler for the session.
        index : int
            file index in the file list.
        ''' 

        self._dh = dataHandler
        self._fileName = self._dh._cars_annos_files[index] # contains an extra 'ca_ims'
        self._shortFileName = os.path.split(self._fileName)[-1]
        
        self.label = self._dh._cars_annos_labels[index]
        self.labelName = self._dh._cars_annos_classnames[self.label]
        self.bbox = self._dh._cars_annos_bbox[index]
        self.isTest = self._dh._cars_annos_isTest[index]
        
        self.pathToImage = os.path.join(self._dh.pathToDataDir, self._fileName)
        for _p in (self.pathToImage,):
            if not os.path.exists(_p):
                raise ValueError('file does not exist: {}'.format(_p))
        
        # updated later
        self.edge = None
        self.bw = None
        self.resampleFilter = None
        self.image = None
        self.patch = None
        # list of PIL.Images - list of patches, using the annotations, taking the smallest square containing it, and resizing.
        
        
    def loadImage(self):
        '''
        '''
        self.image = Image.open(self.pathToImage)
        

    def buildPatch(self, edge=256, bw=True, resampleFilter=Image.BICUBIC):
        '''
        crops images to centered squares.
        
        Inputs
        ------
        edge : int, default 256
            size in pixel of the edge of the *square* patch.
        bw : bool
            whether to turn the image black&white.
        resampleFilter : _
            see PIL.Image.resize().
        '''
        self.edge = edge
        self.bw = bw
        self.resampleFilter = resampleFilter
        
        if self.image is None: self.loadImage()
        
        _im = self.image.copy()
        
        # convert to black&white
        if bw: _im = _im.convert('L')
        
        # change it to square with corresponding center
        [xmin,ymin,xmax,ymax] = self.bbox
    
        xc,yc = int((xmax+xmin)/2),int((ymax+ymin)/2)
        halfedge = int(max((xmax-xmin)/2,(ymax-ymin)/2))
    
        box_square_centered = (xc-halfedge,
                               yc-halfedge,
                               xc+halfedge,
                               yc+halfedge)
        _im = _im.crop(box_square_centered)
        _im = _im.resize((edge,edge))
                
        # return
        self.patch = _im
        
 
    
    def savePatch(self,method='oneDirPerClass'):
        '''
        save the patch to disk
        
        Inputs
        ------
        method : str in ('oneDirPerClass',)
            - 'oneDirPerClass' saves the patch to a directory of the form
              root/macroparam/isTest/labelName/file.png
        '''
        if method == 'oneDirPerClass':
            
            macroparam = ''
            for k in ('edge','bw','resampleFilter'):
                macroparam += k+str(getattr(self,k))
            if self.isTest:
                isTest = 'Test'
            else:
                isTest = 'Train'
            labelName = self.labelName
            
            p = os.path.join(self._dh.pathToDataPatchDir,
                             macroparam,
                             isTest,
                             labelName)
            if not os.path.isdir(p):
                os.makedirs(p)
            self.patch.save(os.path.join(p, self._shortFileName))
            
        else:
            raise NotImplementedError('method not implemented: {}'.format(method))
        
#%% END
      