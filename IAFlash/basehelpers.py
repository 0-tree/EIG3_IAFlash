

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