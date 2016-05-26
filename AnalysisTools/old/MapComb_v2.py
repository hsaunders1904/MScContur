import os, sys
import numpy as np
import matplotlib.pyplot as plt
import colormaps as cmaps
import pickle


maps={}
for root, dirs, files in os.walk('.'):
       for name in files:

		   #walk and look for .map files
           if '.map' in name:
               with open(name,'r+b') as f:
                maps[name.strip(".map")] = pickle.load(f)

#copy the first map in the dictionary, and make it into a blank canvas

data = maps[maps.keys()[0]][:]
for i in range(0,len(data)):
    data[i]=list(data[i])
    data[i][2] = 0.0

for key in maps:
    for i in range(0,len(maps[key])):
        for j in range(0,len(data)):
            if maps[key][i][0] == data[j][0] and maps[key][i][1] == data[j][1]:
                data[j][2] = float(data[j][2]) + float(maps[key][i][2]) ** 2
                #continue

for i in range(0,len(data)):
    data[i][2]= np.sqrt(float(data[i][2]))

#### for some reason I hadcoded the grid width, easy enough to work out
##in fact this whole plotting script is a bit weird and could be done better I think
dx = 25
dy = 50

x_grid_min= min(zip(*data)[1])-dx
y_grid_min= min(zip(*data)[0])-dy
x_grid_max= max(zip(*data)[1])+dx
y_grid_max= max(zip(*data)[0])+dy

yy,xx =np.mgrid[y_grid_min:y_grid_max+dy:2*dy,x_grid_min:x_grid_max+dx:2*dx]
c=np.zeros([len(xx[0,:])-1,len(yy[:,0])-1])


for i in range(0,len(zip(*data)[1])):
    xcounter=0
    ycounter=0
    for xarg2 in xx[1]:
        if zip(*data)[1][i] > xarg2:
            xcounter+=1
    for yarg2 in yy[:,xcounter]:
        if zip(*data)[0][i] > yarg2:
            ycounter+=1
    c[xcounter-1][ycounter-1]=zip(*data)[2][i]


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1,1,1)
#plt.pcolormesh(xx,yy,zz,cmap="seismic", vmin=0, vmax=1)
plt.pcolormesh(xx,yy,c.T,cmap=cmaps.magma_r, vmin=0, vmax=1)
plt.axis([x_grid_min, x_grid_max, y_grid_min, y_grid_max])

plt.rc('text', usetex=True)
plt.rc('font', family='lmodern')
plt.xlabel(r"$M_{\chi}$ [GeV]", fontsize=16)
plt.ylabel(r"$M_{Z'}$ [GeV]", fontsize=16)
plt.rc('text', usetex=False)
plt.rc('font', family='sans')

plt.title("ATLAS + CMS Combined",y=1.02)

plt.colorbar().set_label("CL of exclusion")
plt.savefig("combined.pdf")
plt.savefig("combined.png")


print "end"
