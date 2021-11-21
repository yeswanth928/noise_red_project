#Noise Reduction using Deep Learning

##Introduction
Now video and audio are becoming more and more important that the text and images.
But there's noise everywhere, be it home or public transport etc. But it is necessary for the noise
to be low. So we have developed an application that uses Deep Learning to reduce the noise, and also allow the
users to train the model using their own data. And this application also has a simple interface for the users to
interact with the application.


## Functions

### Noise Reduction
This application has a CNN trained with over 6500 white noise files. And the Deep Learning model got an accuracy of 98%.
Users can use this to reduce white noise. Users can also train model use their own data and save it.
when the audio file is predicted it is saved to project folder in Documents.

### Train Model
There's various kinds of noises in our surroundings not just, so the application gives users an option to create their 
own Deep Learning model by passing the data. And the application automatically saves the model after training.
[Note: Training a model is often time consuming and also requires lot of hardware]

### Extract Audio
It's not always you have an audio file, usually you have a video file, you will want to reduce noise in the video file. 
So the application gives you a feature to extract audio from video in 3 formats .ogg, .wav, .mp3.

### Trim Audio File
As we mentioned earlier Deep Learning is often time and hardware consuming. Imagine a situation where you have an audio 
file of over 30 min, but you want to reduce noise only for a duration of 5 min. So you will be wasting a lot of time and 
a lot of resources. So instead you can trim the audio file and apply noise reduction on the trimmed audio file.

### Spectrogram
Spectrogram is really important when it comes to machine learning using audio file. This application generates 
spectrogram for entire folder of audio files. And it can be used for machine learning or any other operation the user 
wants.

[Note: When the files are processed they are stored in the 'noise_reduction' folder in Documents]

## Installation
* Install python
* Install the python packages in requirements.txt
* Install TensorFlow
* create noise_reduction folder in Documents and put the models' folder in the project in it.
* open cmd in project folder and enter 'python manage.py runserver'

Then it will give you a link through which you can open the website on local machine.

## Technologies Used
* Python
* TensorFlow - used as Deep Learning Library
* Django - Used to create an interface for user and also for backend

[Note: Deep Learning requires a lot of time and resources. So users have to be patient as it may even take hours when 
training the model depending on the data.]
