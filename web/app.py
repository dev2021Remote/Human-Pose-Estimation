import sys
sys.path.insert(0,'..')
import merge_dataset
import os, glob
from flask import  Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import imageio

# Matplot Configuration
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111,projection='3d')

#Function to merge both the dataset files
merge_dataset.mergeFiles('../')


#dataset name
filename = "../pose-output.csv"

# Flask App initiaion
app = Flask(__name__,static_url_path='/static')

error = ''
selected_excersise = ''

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

# Function for connecting keypoints 
def draw_plot3D(keypoints,counter,edges=EDGES):
    
    #FileName
    imgfilename = f'static/images/{counter}.png'


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

    plt.savefig(imgfilename, format='png')

    print(imgfilename,' file created')
    
    plt.cla()

    return imgfilename


# Importing excersise name from the datasest
df = pd.read_csv(filename,usecols=['name'],squeeze=True)
excersises = []

for val in df:
    excersises.append(val.title())

# Function for reading and plotting the graph of particualr excersise
def readAndPlot(index):

    # keypoints to be selected from the file
    arr = ['xX_left_shoulder', 'yY_left_shoulder', 'zZ_left_shoulder', 'xX_right_shoulder', 'yY_right_shoulder', 'zZ_right_shoulder', 'xX_left_elbow', 'yY_left_elbow', 'zZ_left_elbow', 'xX_right_elbow', 'yY_right_elbow', 'zZ_right_elbow', 'xX_left_wrist', 'yY_left_wrist', 'zZ_left_wrist', 'xX_right_wrist', 'yY_right_wrist', 'zZ_right_wrist', 'xX_left_hip', 'yY_left_hip', 'zZ_left_hip', 'xX_right_hip', 'yY_right_hip', 'zZ_right_hip', 'xX_left_knee', 'yY_left_knee', 'zZ_left_knee', 'xX_right_knee', 'yY_right_knee', 'zZ_right_knee', 'xX_left_ankle', 'yY_left_ankle', 'zZ_left_ankle', 'xX_right_ankle', 'yY_right_ankle', 'zZ_right_ankle']

    df = pd.read_csv(filename,usecols=arr,squeeze=True)

    all_points =[]
    for item in arr:

        tes =(df[item][index].split(','))

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
    
    # print(len(allkeypoints[0]))

    
    filenames=[]
    count =0
    totalTestCase = len(allkeypoints)
    inc_Factor = 1 if totalTestCase < 150 else int(totalTestCase/150)
    # print(testcasesLength)
    
    # Looping through Test Cases and saving the images in the static folder
    for i in range(0,totalTestCase,inc_Factor):
        filenames.append(draw_plot3D(allkeypoints[i],count))
        count +=1
        

    print("Total number of images created:  ",len(filenames))

    #Removing the gif files if previously present
    if glob.glob('static/gif/mygif.gif'):
        os.remove('static/gif/mygif.gif')

    with imageio.get_writer('static/gif/mygif.gif', mode='I') as writer:
        for imgfilename in filenames:
            image = imageio.imread(imgfilename)
            writer.append_data(image)

    # deleting all images created
    for imgfilename in set(filenames):
        os.remove(imgfilename)
    

@app.route('/')
def initial():
    global error,selected_excersise
    total = len(excersises)
    print('Total Number of excersise:',total)
    return render_template('index.html',excersises=excersises,total_no_of_excersise=total,message=error, selected_excersise=selected_excersise)

@app.route('/excersiseVisual',methods=['GET', 'POST'])
def showVisualisation():
    index = -1
    global error,selected_excersise,excersises

    if request.method == 'POST':
        index = int(request.form.get('excersise_select'))

    if index == -1:
        error = "Please select the Valid Excersise"
        selected_excersise = ''
    else:
        error = ''
        selected_excersise=excersises[index].upper()

        readAndPlot(index)
        

    print("Index of excersise: ", index)
    
    
    return redirect(url_for('initial'))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == '__main__':

    app.run(host = 'localhost',port=5001, use_reloader = True, debug = True)


