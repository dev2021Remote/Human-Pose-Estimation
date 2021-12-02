
## Human Pose Estimation 

Create a visualization on the basis of the dataset of excersise movement.
Here, dataset is the collection of points that is been collected with the help of the blasepoint, posenet etc.


## Installation


```bash
  pip install -m requirements.txt
```

## Running Application

- For Running a Web Application
```bash
  cd web
  python app.py
```

- For Visualising only
```bash
  python 3D_animation.py
```

## Roadmap

- First, we read the data from the dataset and extracting the keypoints coordinates from it

- Taking each value from the extracted keypoints and plotting it acccrordingly in the graph with the proper edges connection

- Saving the images of each plotted graph and merging it in the gif(animation)

    
## Steps

- Creation of pose-output.csv by merging the pose-output1.csv and pose-output2.csv files.
- Reading the dataset file and extracting all the excersises name form it.
- Extracting the points form the dataset

Points(Columns) we use from the dataest are -
```bash
['xX_left_shoulder', 'yY_left_shoulder', 'zZ_left_shoulder', 'xX_right_shoulder', 'yY_right_shoulder', 'zZ_right_shoulder', 'xX_left_elbow', 'yY_left_elbow', 'zZ_left_elbow', 'xX_right_elbow', 'yY_right_elbow', 'zZ_right_elbow', 'xX_left_wrist', 'yY_left_wrist', 'zZ_left_wrist', 'xX_right_wrist', 'yY_right_wrist', 'zZ_right_wrist', 'xX_left_hip', 'yY_left_hip', 'zZ_left_hip', 'xX_right_hip', 'yY_right_hip', 'zZ_right_hip', 'xX_left_knee', 'yY_left_knee', 'zZ_left_knee', 'xX_right_knee', 'yY_right_knee', 'zZ_right_knee', 'xX_left_ankle', 'yY_left_ankle', 'zZ_left_ankle', 'xX_right_ankle', 'yY_right_ankle', 'zZ_right_ankle']
```

- Changing dataest into a (x,y,z) coordinates so that we can use it to plot the diagram

Dataset Examples -
```bash
[0.5418540835380554, 0.3002445101737976, -0.012251616455614567]
[0.5088052749633789, 0.3219769299030304, 0.023481255397200584]
.
...
```

- Now we accumulate the coordinates of all 12 keypoints for each testcases

Keypoints are -
```bash
[ left Shoulder, right shoulder, left elobw, right elbow, left wrist, right hip, left knee, right knee, left ankle, right ankle ]
```
![Keypoints](https://github.com/dev2021Remote/posenet/blob/main/PosenetPoints.png)

`[Edges/Connections b/w keypoints are formed according to the image]`
- Once all the 12 keypoints are accumulated we plot the graph and save it in the image(png format)
- And saving each plotted graph into the image in `/static/images` folder. (We are restricting the image creation upto 150 files only)
- As the image created we create the short animation(gif) with the ImageIo and integrate it with front-end
- Now we delete all the images that are created while plotting the graph




