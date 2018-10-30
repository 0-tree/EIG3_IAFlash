

import os
import re
from PIL import Image
import xml.etree.ElementTree
import scipy.io # used to import .mat files with scipy.io.loadmat (see [here](https://stackoverflow.com/questions/874461/read-mat-files-in-python))




#%%

class DataHandler:
    
    def __init__(self, pathToDataDir, whichList):
        '''
        Inputs
        ------
        pathToDataDir : str
            path to the directory containing Images/ Annotations/ Lists/ etc.
        whichList : str, in ('all','train','test')
            which list of files should be used.    
        Notes
        -----
        - this class assumes no change is made in the structure of the
          directory downloaded from http://vision.stanford.edu/aditya86/ImageNetDogs/
          nor in files names
        - except: Annotation/ <- Annotation*s*/
        '''

        self.whichList = whichList
        self.pathToDataDir = pathToDataDir   
        self.pathToDataImageDir = os.path.join(pathToDataDir,'Images')
        self.pathToDataAnnotationDir = os.path.join(pathToDataDir,'Annotations')
        self.pathToDataListDir = os.path.join(pathToDataDir,'Lists')

        for _p in (self.pathToDataDir,
                   self.pathToDataImageDir,
                   self.pathToDataAnnotationDir,
                   self.pathToDataListDir):
            if not os.path.isdir(_p):
                raise ValueError('directory does not exist: {}'.format(_p))

        self._loadLists()
        self.n = len(self._fileList_file)
        

    def _loadLists(self):
        '''
        '''
        if self.whichList == 'all':
            _name = 'file'
        elif self.whichList == 'train':
            _name = 'train'
        elif self.whichList == 'test':
            _name = 'test'
        else:
            raise ValueError('unkown whichList: {}'.format(self.whichList))
            
        _list = scipy.io.loadmat(os.path.join(self.pathToDataListDir,_name+'_list.mat'))
        self._fileList_file = [x[0][0] for x in _list['file_list']]
        self._fileList_annotation = [x[0][0] for x in _list['annotation_list']]
        self._fileList_label = [x[0] for x in _list['labels']]
            
    
    
#%%
                
class ImageWorker:
    
    def __init__(self, dataHandler, indexInList):
        '''
        Inputs
        ------
        dataHandler : DataHandler
            DataHandler for the session.
        indexInList : int
            file index in the file list.
        ''' 

        _fileName = dataHandler._fileList_file[indexInList]
        _annotationName = dataHandler._fileList_annotation[indexInList]
        self.label = dataHandler._fileList_label[indexInList]
        
        self.pathToImage = os.path.join(dataHandler.pathToDataImageDir, _fileName)
        self.pathToAnnotation = os.path.join(dataHandler.pathToDataAnnotationDir, _annotationName)

        for _p in (self.pathToImage,
                   self.pathToAnnotation):
            if not os.path.exists(_p):
                raise ValueError('file does not exist: {}'.format(_p))
                
        # get the label from .pathToImage (can also use the lists.mat...)
        _dir = os.path.normpath(self.pathToImage).split(os.sep)[-2]
        self.labelName = re.findall('-(.*)',_dir)[0]
        
        # hard code
        self.bndboxMarker = './/bndbox'
        
        # updated later
        self.image = None
        self.annotation = None
        self.patches = None
        # list of PIL.Images - list of patches, using the annotations, taking the smallest square containing it, and resizing.
        
        
    def loadImage(self):
        '''
        '''
        self.image = Image.open(self.pathToImage)
        
        
    def loadAnnotation(self):
        '''
        '''
        self.annotation = xml.etree.ElementTree.parse(self.pathToAnnotation)
        
        
    def buildPatches(self, edge=256, resampleFilter=Image.BICUBIC):
        '''
        crops images to centered squares.
        
        Inputs
        ------
        edge : int, default 256
            size in pixel of the edge of the *square* patch.
        resampleFilter : _
            see PIL.Image.resize().
        '''
        if self.image is None: self.loadImage()
        if self.annotation is None: self.loadAnnotation()
            
        self.patches = []
        allbndbox = self.annotation.findall(self.bndboxMarker)
        for bndbox in allbndbox:
            
            # get the box
            [xmin,ymin,xmax,ymax] = [int(e.text) for e in bndbox.getchildren()]
            
            # change it to square with corresponding center
            xc,yc = int((xmax+xmin)/2),int((ymax+ymin)/2)
            halfedge = int(max((xmax-xmin)/2,(ymax-ymin)/2))
            
            box_square_centered = (xc-halfedge,
                                   yc-halfedge,
                                   xc+halfedge,
                                   yc+halfedge)
            im_crop = self.image.crop(box_square_centered)
            im_patch = im_crop.resize((edge,edge),resampleFilter)
            
            self.patches.append(im_patch)
                
    
    
#%% END
      