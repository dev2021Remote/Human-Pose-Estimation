import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
# import SimpleITK as sitk
import cv2

interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
interpreter.allocate_tensors()

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    # (6, 12): 'c',
    # (11, 12): 'y',
    # (11, 13): 'm',
    # (13, 15): 'm',
    # (12, 14): 'c',
    # (14, 16): 'c'
}

def draw_keypoints(frame,keypoints,confidence_threshold):
    y,x,c = frame.shape
    # print(c)
    shaped = np.squeeze(np.multiply(keypoints,[y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        # if kp_conf > confidence_threshold:
        cv2.circle(frame,(int(kx), int(ky)),4,(0,255,0),-1)

def draw_connections(frame,keypoints,edges,confidence_threshold):
    y,x,c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints,[y,x,1]))
    
    for edge,color in edges.items():
        p1,p2 = edge
        y1,x1,c1  = shaped[p1]
        y2,x2,c2 = shaped[p2]
        
        # if (c1 > confidence_threshold) & (c2 >  confidence_threshold):
        cv2.line(frame,(int(x1),int(y1)),(int(x2),int(y2)),(255,0,0),2)

def draw_connections_3d(ax,points,edjes):
    print(points,len(points))
    for edje,color in edjes.items():
        p1,p2 = edje
        x,y,z=[],[],[]
        x.append(points[p1][0]*480)
        x.append(points[p2][0]*480)

        y.append(points[p1][1]*640)
        y.append(points[p2][1]*640)

        z.append(points[p1][2])
        z.append(points[p2][2])
        print(x,y,z)
        ax.plot(x,y,z,color="black")


arr = [[0.5418540835380554,0.3002445101737976,0.012251616455614567],
    [0.5088052749633789,0.3219769299030304,0.29006227850914],
    [0.5200956463813782,0.43313315510749817,0.023481255397200584],
    [0.48235487937927246,0.4504028856754303,0.34773996472358704],
    [0.5298163294792175,0.5152466893196106,0.053506262600421906],
    [0.4858378767967224,0.5662975907325745,0.37318840622901917],
    [0.5519704818725586,0.5113722085952759,0.09740140289068222],
    [0.5347285866737366,0.544847309589386,0.0975169762969017],
    [0.6598052382469177,0.48735326528549194,0.07413876801729202],
    [0.6464101076126099,0.525979220867157,0.1422564834356308 ],
    [0.6857618689537048	,0.6739863157272339	, 0.19033436477184296],
    [0.6738548278808594,0.7142422795295715,0.026912769302725792]
    ]

cap = cv2.VideoCapture(0)
# ax = plt.axes(projection='3d')
while cap.isOpened():
    ret, frame = cap.read()
    
    
    # Image Reshaping
    img = frame.copy()
    
    #white background
    img_3 = np.zeros([480,640,3],dtype=np.uint8)
    img_3.fill(255)

    # print(img.shape)
    img = tf.image.resize(np.expand_dims(img,axis=0),size=(192,192))
    
    input_image = tf.cast(img,dtype=tf.float32)
    
    #input and output
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    
    # prdecting 
    interpreter.set_tensor(input_details[0]['index'],np.array(input_image))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    # print(keypoints_with_scores)
    
    
    ### point form csv file
    draw_connections(img_3,arr,EDGES,0.1)
    draw_keypoints(img_3,arr,0.1)

    # webcam input points 
    # draw_connections(img_3,keypoints_with_scores,EDGES,0.4)
    # draw_keypoints(img_3,keypoints_with_scores,0.3)
    
    #actual image
    # cv2.imshow('Movenet Lightinig',frame)
    # plt.show()

    #pose with points
    cv2.imshow('Points and edjes Only',img_3)
    # cv2.imshow('Points and edjes Only',frame)


    if cv2.waitKey(10) & 0xFF==ord('q'):
        
        break


# print(frame.shape)
# tes = (np.squeeze(keypoints_with_scores)
tes = (np.squeeze(arr))

# print(len(tes))
x,y,z=[],[],[]
for item in tes:
    x.append(item[0]*480)
    y.append(item[1]*640)
    z.append(item[2])
# print(x)

# for 3d points
# ax.plot3D(x,y,z)

# for 3d points scatter 
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(x,y,z,c='red')
draw_connections_3d(ax,tes,EDGES)
# ax.plot(x, y, z, color='black')

plt.show()
cap.release()
cv2.destroyAllWindows()

