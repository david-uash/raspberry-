{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import math\n",
    "import numpy as np\n",
    "import cv2\n",
    "import matplotlib.pyplot as plt\n",
    "from PIL import Image\n",
    "import random\n",
    "\n",
    "import keras\n",
    "from keras.models import Sequential\n",
    "from keras.layers import Convolution2D \n",
    "from keras.layers import Conv2D\n",
    "from keras.layers import MaxPooling2D\n",
    "from keras.layers import Flatten\n",
    "from keras.layers import Dense"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "### INIT CNN ###\n",
    "vector = np.array((0,0,0))\n",
    "###########\n",
    "### CNN ###\n",
    "###########\n",
    "inputshape = vector.shape\n",
    "model2 = Sequential()\n",
    "model2.add(Dense(12,input_dim=3,activation='relu'))\n",
    "model2.add(Dense(32,activation='relu'))\n",
    "model2.add(Dense(9,activation='relu'))\n",
    "#model2.add(Dense(64,activation='relu'))\n",
    "#model2.add(Dense(32,activation='relu'))\n",
    "model2.add(Dense(units=1,activation='sigmoid')) #min_value=0, max_value=1\n",
    "model2.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])\n",
    "#model2.compile(loss='CategoricalCrossentropy',optimizer='adam',metrics=['accuracy'])\n",
    "#model2.compile(loss='mean_squared_error',optimizer='adam',metrics=['mse'])\n",
    "print(\"the prediction for vector is: \",model2.predict(vector.reshape(1,3)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "pole_length = 0.3 #[m]\n",
    "angle=0\n",
    "time_interval = 0.05 #[sec]\n",
    "g=9.8 #[m/s^2]\n",
    "ball_mass = 0.005 #[kg]\n",
    "ball_radius = 0.025 #[m]\n",
    "friction_coefficient = 0.2\n",
    "v0 = 0\n",
    "x0 = 0 #[m]\n",
    "min_angle=-8 #[deg]\n",
    "max_angle=-8 #[deg]\n",
    "height,width=240,640\n",
    "length = 610\n",
    "image = np.ones((height, width)) * 255\n",
    "\n",
    "\n",
    "sucess_time = 10 #[sec]\n",
    "gamma = 0.9\n",
    "wins = 0\n",
    "loss = 0\n",
    "x_train,y_train = [],[]\n",
    "i_step_in_current_round = 0 \n",
    "i_step_in_total_from_beginning = 0 \n",
    "num_of_round = 0 \n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def predict2degree(degreeAsFloat):\n",
    "    mydegree = np.round((degreeAsFloat[0]-0.5)*10)\n",
    "    return mydegree\n",
    "\n",
    "def drawImage(ballPosition,lineAngle):\n",
    "    #draw line\n",
    "    image = np.ones((height, width)) * 255\n",
    "    normalize_x = ballPosition\n",
    "    angle = lineAngle\n",
    "    x_center, y_center = int(width/2), int(height/2)\n",
    "    x2 = x_center+int(length/2*math.cos(angle))\n",
    "    y2 = y_center+int(length/2*math.sin(angle))\n",
    "    x1,y1 = (x_center-int(length/2*math.cos(angle))),(y_center-int(length/2*math.sin(angle)))\n",
    "    line_thickness = 2\n",
    "    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), thickness=line_thickness)\n",
    "    \n",
    "    M = (y2-y1)/(x2-x1)\n",
    "    y_center_of_circle = M*normalize_x + y1 -M*x1\n",
    "    \n",
    "    #draw circle\n",
    "    radius = 10\n",
    "    center_coordinates = (int(normalize_x),int(y_center_of_circle+radius))\n",
    "    color = (0, 255, 0)\n",
    "    thickness = 2\n",
    "    image = cv2.circle(image, center_coordinates, radius, color, thickness)\n",
    "    \n",
    "    \n",
    "    font                   = cv2.FONT_HERSHEY_SIMPLEX\n",
    "    my_left_point          = (width-30,height-30)\n",
    "    my_right_point         = (30,height-30)\n",
    "    fontScale              = 1\n",
    "    fontColor              = (0,0,0)\n",
    "    lineType               = 2\n",
    "    \n",
    "    if(lineAngle > 0):\n",
    "        cv2.putText(image,'|',my_left_point,font,fontScale,fontColor,lineType)\n",
    "    else:\n",
    "        cv2.putText(image,'|-',my_right_point,font,fontScale,fontColor,lineType)\n",
    "    image = np.flip(image)\n",
    "    \n",
    "\n",
    "    return image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "from os import mkdir,makedirs\n",
    "MODELVERESION=\"005_randrange\"\n",
    "MODELPATH=\"/tmp/model_weights_sigmoid_\"+MODELVERESION\n",
    "MODELNAME=\"simolator\"+MODELVERESION\n",
    "if not os.path.exists(MODELPATH):\n",
    "    makedirs(MODELPATH)\n",
    "    makedirs(MODELPATH+\"/weights\")\n",
    "    makedirs(MODELPATH+\"/model\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#from keras.models import load_model\n",
    "##model2 = load_model(\"/tmp/model_weights_sigmoid_004_randrange/model/simolator004_randrange\")\n",
    "#model2 = load_model(MODELPATH+\"/model/\"+MODELNAME)\n",
    "                    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "model_prediction = predict2degree(model2.predict(vector.reshape(1,3)))\n",
    "degree = round((model_prediction[0]-0.5)*10)\n",
    "new_degree = round((model_prediction[0]-0.5)*10)+1\n",
    "\n",
    "#print(\"init degree\",degree)\n",
    "print(\"starting\")\n",
    "num_of_round=0\n",
    "gamesToPlay=20000\n",
    "while(num_of_round<gamesToPlay):\n",
    "    x_train,y_train = [],[]\n",
    "    degree,new_degree=0,0\n",
    "    x0=((random.random()-0.5)*2)/2\n",
    "    v0=((random.random()-0.5)*2)/4\n",
    "    #vector = np.array((0,0,0))\n",
    "    #x_train.append(vector)\n",
    "    model_prediction=0\n",
    "    original_y=[]\n",
    "    num_of_round+=1\n",
    "    print(\"round number:\",num_of_round)\n",
    "    mystack = [np.ones((height, width)) * 255]\n",
    "    #print(\"type(degree)\",type(degree))\n",
    "    for i in range(0,500):\n",
    "        if(random.random() < math.exp(-num_of_round/(gamesToPlay*0.4))):\n",
    "            new_degree=random.random()\n",
    "            # print(\"randomize degree\",degree)\n",
    "            #new_degree = round((new_degree-0.5)*10)\n",
    "            new_degree = random.randrange(-8,9)\n",
    "        else:\n",
    "            p=1\n",
    "            #print(\"degree is not randomize for this round\")\n",
    "            #new_degree = degree\n",
    "        #degree = int(degree)\n",
    "        \n",
    "        #print(\"degree:\",degree)\n",
    "        #print(\"new_degree:\",new_degree)\n",
    "        if(new_degree == 0):\n",
    "            randDegree = random.randrange(0,2)\n",
    "            if(randDegree==0):\n",
    "                new_degree = -1\n",
    "            else:\n",
    "                new_degree = 1\n",
    "        if(new_degree != degree):\n",
    "            #print(\"degrees not equal\")\n",
    "            if(new_degree>degree):\n",
    "                loopsign=+1\n",
    "            else:\n",
    "                loopsign=-1\n",
    "            save_new_degree=new_degree\n",
    "            while(abs(int(new_degree)-int(degree))>0):    \n",
    "                #print(\"degree in loop:\",degree)\n",
    "                degree = degree+(1*loopsign)\n",
    "                #print(\"degree changing\",degree)\n",
    "                #change_sloop_slowly\n",
    "                angle=math.pi*(int(degree)/180)\n",
    "                acceleration = (3/5)*g*math.sin(angle)\n",
    "                current_v = v0 + acceleration*time_interval \n",
    "                current_x = x0 + v0*time_interval + (1/2)*acceleration*(time_interval**2)\n",
    "                v0 = current_v\n",
    "                x0 = current_x\n",
    "                normalize_x = 300-current_x*300/1.5\n",
    "                #print(\"after\",time_interval,\"[sec], at angle=\",angle*180/math.pi,\"[deg], the ball moved to \",current_x)\n",
    "                #print(\"angle\",angle)\n",
    "                if(num_of_round==gamesToPlay):\n",
    "                    image = drawImage(normalize_x,angle)\n",
    "                    mystack = np.concatenate((mystack,[image]),axis=0)\n",
    "            #print(\"degree at end of loop:\",degree)\n",
    "\n",
    "        else:\n",
    "            for j in range(1,4):\n",
    "                angle=math.pi*(int(degree)/180)\n",
    "                acceleration = (3/5)*g*math.sin(angle)\n",
    "                current_v = v0 + acceleration*time_interval \n",
    "                current_x = x0 + v0*time_interval + (1/2)*acceleration*(time_interval**2)\n",
    "                v0 = current_v\n",
    "                x0 = current_x\n",
    "                normalize_x = 300-current_x*300/1.5\n",
    "                #print(\"after\",time_interval,\"[sec], at angle=\",angle*180/math.pi,\"[deg], the ball moved to \",current_x)\n",
    "                #print(\"angle\",angle)\n",
    "                if(num_of_round==gamesToPlay):\n",
    "                    image = drawImage(normalize_x,angle)\n",
    "                    mystack = np.concatenate((mystack,[image]),axis=0)\n",
    "        #print(\"degree for i\",i,\"move is:\",degree)\n",
    "        \n",
    "       \n",
    "        #print(\"degree before predict:\",degree)\n",
    "        vector = np.array((degree/8,normalize_x/600,current_v/10))\n",
    "        model_prediction = model2.predict(vector.reshape(1,3))\n",
    "        new_degree = np.round((model_prediction[0]-0.5)*16)\n",
    "        #print(\"model_prediction\",model_prediction)\n",
    "       \n",
    "        x_train.append(vector)\n",
    "        y_train.append(model_prediction)\n",
    "    \n",
    "        #print(\"vector\",vector)\n",
    "        #print(\"model_prediction:\",model_prediction,\" <==> degree:\",degree)\n",
    "        \n",
    "        \n",
    "        \n",
    "        if((normalize_x > 600) or (normalize_x < 10)):\n",
    "            break\n",
    "        if(i*time_interval >=sucess_time):\n",
    "            break\n",
    "           \n",
    "    print(\"game ended after\",i,\"steps\")\n",
    "    #print(\"y_train:\",y_train)\n",
    "    x0=((random.random()-0.5)*2)/2\n",
    "    v0=((random.random()-0.5)*2)/6\n",
    "    original_y = y_train.copy()\n",
    "    \n",
    "    if(i*time_interval >= sucess_time):\n",
    "        print(\"model ended without ball falling\")\n",
    "    elif((normalize_x > 600) or (normalize_x < 10)):\n",
    "        print(\"game ended becouse ball dropped\")\n",
    "        if(len(y_train)<25):\n",
    "            #print(\"y_train\",y_train)\n",
    "            for j in range(1,len(y_train),1): \n",
    "                y_train[len(y_train)-j] = (1-y_train[len(y_train)-j])\n",
    "            #print(\"original_y\",original_y)\n",
    "            \n",
    "        else:\n",
    "            if(len(y_train)>90):\n",
    "                 for j in range(1,30,1): \n",
    "                    y_train[len(y_train)-j] = (1-y_train[len(y_train)-j])\n",
    "            elif(len(y_train)>65):\n",
    "                for j in range(1,20):\n",
    "                    y_train[len(y_train)-j] = (1-y_train[len(y_train)-j])\n",
    "            else:\n",
    "                for j in range(1,int(len(y_train)*0.8),1): \n",
    "                    y_train[len(y_train)-j] = (1-y_train[len(y_train)-j])\n",
    "        numToChange = random.randrange(0,7)            \n",
    "        for j in range(0,numToChange):\n",
    "            numToChange =  random.randrange(1,int(len(y_train)-1))\n",
    "            y_train[numToChange] = (1-y_train[numToChange])\n",
    "    #print(\"y_train:\",y_train)\n",
    "    model2.fit(x=np.vstack(x_train),y=np.vstack(y_train))\n",
    "    if(num_of_round%1000==0):\n",
    "        model2.save_weights(MODELPATH+\"/weights/\"+MODELNAME)\n",
    "        model2.save(MODELPATH+\"/model/\"+MODELNAME)\n",
    "    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import imageio; \n",
    "from IPython.display import Video; \n",
    "edges = mystack\n",
    "imageio.mimwrite('test2.mp4', edges, fps=30); \n",
    "Video('test2.mp4', width=640, height=480)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(MODELPATH+\"/\"+MODELVERESION+\".mp4\")\n",
    "imageio.mimwrite(MODELPATH+\"/\"+MODELVERESION+\".mp4\", edges, fps=33); \n",
    "\n",
    "#from os import mkdir,makedirs\n",
    "#MODELVERESION=\"007\"\n",
    "#MODELPATH=\"/tmp/model_weights_\"+MODELVERESION\n",
    "#MODELNAME=\"simolator\"+MODELVERESION\n",
    "#makedirs(MODELPATH)\n",
    "#makedirs(MODELPATH+\"/weights\")\n",
    "#makedirs(MODELPATH+\"/model\")\n",
    "#\n",
    "#model2.save_weights(MODELPATH+\"/weights/\"+MODELNAME)\n",
    "#model2.save(MODELPATH+\"/model/\"+MODELNAME)\n",
    "\n",
    "#x_train\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "angle=math.pi*(int(degree)/180)\n",
    "angle=math.pi*(int(degree)/180)\n",
    "acceleration = (3/5)*g*math.sin(angle)\n",
    "current_v = v0 + acceleration*time_interval \n",
    "current_x = x0 + v0*time_interval + (1/2)*acceleration*(time_interval**2)\n",
    "v0 = current_v\n",
    "x0 = current_x\n",
    "normalize_x = 300-current_x*300/1.5\n",
    "#print(\"after\",time_interval,\"[sec], at angle=\",angle*180/math.pi,\"[deg], the ball moved to \",current_x)\n",
    "#print(\"angle\",angle)\n",
    "if(num_of_round==gamesToPlay):\n",
    "    image = drawImage(normalize_x,angle)\n",
    "    mystack = np.concatenate((mystack,[image]),axis=0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "degree=0\n",
    "normalize_x=0\n",
    "current_v=0\n",
    "vector = np.array((degree/5,normalize_x/600,current_v/10))\n",
    "model_prediction = model2.predict(vector.reshape(1,3))\n",
    "new_degree = np.round((model_prediction[0]-0.5)*10)\n",
    "#print(model_prediction[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import random\n",
    "for i in range(0,20):\n",
    "    print(random.randrange(-5,6))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
