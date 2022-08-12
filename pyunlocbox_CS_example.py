import matplotlib.image as mpimg
import numpy as np
from pyunlocbox import solvers
from pyunlocbox import functions
import matplotlib.pyplot as plt

img = np.load('C:/users/jaris/documents/Coded ultrafast imaging (compressed ultrafast photography)/smiley_face.npy')
img=mpimg.imread('C:/users/jaris/pictures/test DIII-D.jpg')
img=img.sum(axis=2)
img=img[200:400,200:400]
img=img/img.max()


mask = np.random.uniform(size=img.shape)

mask[mask<0.8]=0
mask[mask>0]=1

g = lambda x: (mask * x)
imgm=g(img)

f1 = functions.norm_tv(maxit=50, dim=2)
tau = 100
f2 = functions.norm_l2(y=imgm, A=g, lambda_=tau)
solver = solvers.forward_backward(step=0.5/tau)
x0 = np.array(imgm)  # Make a copy to preserve im_masked.
ret = solvers.solve([f1, f2], x0, solver)


plt.close('all')
fig = plt.figure(figsize=(8, 2.5))
ax1 = fig.add_subplot(1, 3, 1)
_ = ax1.imshow(img, cmap='gray')
_ = ax1.axis('off')
_ = ax1.set_title('Original image')
ax2 = fig.add_subplot(1, 3, 2)
_ = ax2.imshow(imgm, cmap='gray')
_ = ax2.axis('off')
_ = ax2.set_title('Masked image')
ax3 = fig.add_subplot(1, 3, 3)
_ = ax3.imshow(ret['sol'], cmap='gray')
_ = ax3.axis('off')
_ = ax3.set_title('Reconstructed image')
