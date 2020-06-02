# -*- coding: utf-8 -*-
"""e_g.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mCwRMGtQc3o3MkNU3MX3GkSxZMvP2WcZ
"""

import struct as st
import numpy as np               
                  
MNIST = {'MY_IMGS':'train-images.idx3-ubyte'}
train_imagesfile = open(MNIST['MY_IMGS'],'rb')
train_imagesfile.seek(0)
magic = st.unpack('>4B',train_imagesfile.read(4))
number_of_images,number_of_rows,number_of_columns=st.unpack('>III',train_imagesfile.read(12))
temp=np.asarray(st.unpack('>'+(number_of_images*number_of_rows*number_of_columns)*'B',train_imagesfile.read(number_of_images*number_of_rows*number_of_columns)))
images_array=temp.reshape(number_of_images,number_of_rows,number_of_columns)

print(images_array)

import struct as st
import numpy as np               
                  
MNIST = {'MY_LABELS':'train-labels.idx1-ubyte'}
train_labelsfile = open(MNIST['MY_LABELS'],'rb')
train_labelsfile.seek(0)
magic = st.unpack('>4B',train_labelsfile.read(4))
number_of_items=st.unpack('>I',train_labelsfile.read(4))
temp=(st.unpack('>'+60000*'B',train_labelsfile.read(60000)))

print(temp)

import numpy as np

R=[]
for img in images_array:
  temp2=np.array(img.flatten())
  R.append(temp2)

#flattend image array
R=np.array(R)

##Library function of Standard Scalar

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(R)

std_data=(scaler.transform(R))

y=(std_data[0].reshape(28,28))
import matplotlib.pyplot as plt
plt.imshow(y[:,:], cmap='gray')
plt.show()

from scipy.linalg import eigh
import pandas as pd
covariance_matrix=np.cov(R.T)

##For P dimensional reduction####
values, vectors = eigh(covariance_matrix)
values=np.flipud(values)
#vectors=np.flipud(vectors)

vectors=vectors.T
vectors=np.flipud(vectors)

eigen_energy=input("Enter eigen energy value in fraction")
eigen_energy=float(eigen_energy)
N=0
for i in range(0,784):
  N=N+values[i]
frac=0
p=0
for i in range(0,784):
  frac=frac+(values[i]/N)
  if frac > eigen_energy:
    p=i
    break

print(p)

vect_upd=[]
for i in range(0,p):
  vect_upd.append(vectors[i])
  
vect_upd=np.array(vect_upd)

projected_X = np.matmul(vect_upd,std_data.T)


projected_X=projected_X.T

print(len(projected_X))
print((temp[i]))

####LDA####
##################




classes = [[] for i in range(10)]

for i in range(60000):
  index=temp[i]
  classes[index].append(projected_X[i])
  
for i in range(0,len(classes)):
  classes[i]=np.array(classes[i])
classes=np.array(classes)



cov_array=[]
mean=[]
prior=[]

def mean_calc(group):
  
  mean=[]

  for j in range(0,len(group[0])):
    sum=0
    for i in range(0,len(group)):
      sum =sum+group[i][j]
    sum=sum/len(group)
    mean.append(sum)

  mean=np.array(mean)
  return mean

S1 = (len(classes[0])*np.cov(classes[0].T))/len(R)
mean.append(mean_calc(classes[0]))
for i in range(1,10):
  c= (len(classes[i])*(np.cov(classes[i].T)))/len(R)
  S1=S1+c
  mean.append(mean_calc(classes[i]))


for i in range(0,10):
  prior.append(len(classes[i])/60000)

S_INV=np.linalg.pinv(S1.T)
S_DET=np.linalg.det(S1)


import struct as st
import numpy as np               
                  
MNIST = {'MY_IMGS':'t10k-images.idx3-ubyte'}
test_imagesfile = open(MNIST['MY_IMGS'],'rb')
test_imagesfile.seek(0)
magic = st.unpack('>4B',test_imagesfile.read(4))
number_of_images,number_of_rows,number_of_columns=st.unpack('>III',test_imagesfile.read(12))
#temp=np.asarray(st.unpack('>'+(number_of_images*number_of_rows*number_of_columns)*'B',test_imagesfile.read(number_of_images*number_of_rows*number_of_columns)))
#images_array_test=temp.reshape(number_of_images,number_of_rows,number_of_columns)
temp=np.asarray(st.unpack('>'+(10000*number_of_rows*number_of_columns)*'B',test_imagesfile.read(10000*number_of_rows*number_of_columns)))
images_array_test=temp.reshape(10000,number_of_rows,number_of_columns)


#print(images_array_test)
import numpy as np

S=[]
for img in images_array_test:
  temp=np.array(img.flatten())
  S.append(temp)

#flattend image array for testing
S=np.array(S)

scaler = StandardScaler()
scaler.fit(S)

S=(scaler.transform(S))


S = np.matmul(vect_upd,S.T)


S=S.T


#####Test Data label Extraction####
import struct as st
import numpy as np               
                  
MNIST = {'MY_LABELS':'t10k-labels.idx1-ubyte'}
test_labelsfile = open(MNIST['MY_LABELS'],'rb')
test_labelsfile.seek(0)
magic = st.unpack('>4B',test_labelsfile.read(4))
number_of_items=st.unpack('>I',test_labelsfile.read(4))
temp1=(st.unpack('>'+10000*'B',test_labelsfile.read(10000)))

print(temp1)
print((S_INV))
print((S_DET))

###LDA CODE ####

correct=0


for index in range(0,len(S)):
  G_max=-99999999
  cls=-1
  for i in range(0,10):
    p1=-0.5 * np.log(S_DET)
    t=(S[index]-mean[i])
    
    q=np.matmul(t.T ,S_INV)
    p2=-0.5 *(np.matmul(q.T,t))

    p3= np.log(prior[i])

    G = p1+p2 +p3
    #print(G)
    if(G>G_max):
      G_max=G
      cls=i 
  #print(cls)    
  if temp1[index]==cls:
    #print(cls)
    correct =correct+1

###0.95 eigen energy
Accuracy=correct/10000
print(Accuracy)

###0.70 eigen energy
Accuracy=correct/10000
print(Accuracy)

###0.90 eigen energy
Accuracy=correct/10000
print(Accuracy)

###0.99 eigen energy
Accuracy=correct/10000
print(Accuracy)