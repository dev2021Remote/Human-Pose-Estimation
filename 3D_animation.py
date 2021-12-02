from merge_dataset import mergeFiles
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.animation import FuncAnimation
import time
import pandas as pd

# %matplotlib notebook
plt.rcParams['animation.html'] = 'jshtml'

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111,projection='3d')

# Merging dataset files into one
mergeFiles()

# Connection between keypoints
EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'm',
    (3, 5): 'c',
    (0, 6): 'm',
    (1, 7): 'c',
    (6, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (9, 11): 'y',
}


# Function for Drawing keypoints and connections b/w keypoints
def draw_plot(keypoints,edges=EDGES):
    # print(keypoints)
    x,y,z=[],[],[]
    for val in keypoints:
        x.append(val[0])
        y.append(val[1])
        z.append(val[2])
    
    for edge,color in edges.items():
        p1,p2 = edge
        X = [x[p1],x[p2]]
        Y = [y[p1],y[p2]]
        Z = [z[p1],z[p2]]

        ax.plot(X,Y,Z,color='b')

# Importing dataset and reading the data from keypoints
arr = ['xX_left_shoulder', 'yY_left_shoulder', 'zZ_left_shoulder', 'xX_right_shoulder', 'yY_right_shoulder', 'zZ_right_shoulder', 'xX_left_elbow', 'yY_left_elbow', 'zZ_left_elbow', 'xX_right_elbow', 'yY_right_elbow', 'zZ_right_elbow', 'xX_left_wrist', 'yY_left_wrist', 'zZ_left_wrist', 'xX_right_wrist', 'yY_right_wrist', 'zZ_right_wrist', 'xX_left_hip', 'yY_left_hip', 'zZ_left_hip', 'xX_right_hip', 'yY_right_hip', 'zZ_right_hip', 'xX_left_knee', 'yY_left_knee', 'zZ_left_knee', 'xX_right_knee', 'yY_right_knee', 'zZ_right_knee', 'xX_left_ankle', 'yY_left_ankle', 'zZ_left_ankle', 'xX_right_ankle', 'yY_right_ankle', 'zZ_right_ankle']
filename = "test_data.csv"
df = pd.read_csv(filename,usecols=arr,squeeze=True)

all_points =[]
for item in arr:
    # tes =(df[item][Index of the Excersise].split(','))
    tes =(df[item][0].split(','))

    total_val =(len(tes))
    val =[]

    for i in tes:
        temp = i
        if i.find("[")>=0 or i.find("]")>=0:
            temp = temp.replace("[","")
            temp = temp.replace("]","")

        val.append(float(temp))
    
    
    all_points.append(val)
    
print("total number of testcases : ",len(all_points[0]))  

allkeypoints = []
threshold_value = 0
count = 0

for i in range(len(all_points[0])):
    temp = []
    for j in range(0,36,3):
        temp.append([all_points[j][i],all_points[j+1][i],all_points[j+2][i]])
        threshold_value +=all_points[j+2][i]
        count +=1
        
    allkeypoints.append(temp)
    

# Looping through Test Cases and visualizing the animation
for val in allkeypoints:
    print(val)


    draw_plot(val)
    
    #To pause the graph for the next frame
    plt.pause(0.001)
    plt.cla()

    if 0xFF==ord('q'):
        break

#for ploting the last cordinates
draw_plot(val)

plt.show()



