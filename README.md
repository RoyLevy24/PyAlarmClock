# PyAlarmClock

Welcome to PyAlarmClock<br><br>This is a python based alarm clock that uses face and speech recognition in order to turn off alarms.

### Installation
---
1. Make sure you have python 3.6 version or above.
2. Clone this repository.
3. Navigate to the main folder contaning requirements.txt (PyAlarmClock).
4. Open up a terminal in the current folder.
5. First, install cmake using pip by typing the following command: ***pip install cmake==3.18.4.post1***
6. Second, install all the requirements using pip by typing the following command: ***pip install -r requirements.txt***

### Troubleshooting
---
If you are experiencing any issues with the installation process this might have to do with these libraries:
1. PyAudio
2. dlib

For **PyAudio** we recommand downloading the wheel file from the following link:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

then using ***pip install wheel_file_name*** to install the file downloaded (wheel_file_name is a placeholder for the name of the wheel you've downloaded).

For **dlib** we recommand refering to the following links for troubleshooting:<br>
•	https://www.youtube.com/watch?v=xaDJ5xnc8dc&ab_channel=Pythoholic<br>
•	https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f<br>
•	https://www.learnopencv.com/install-dlib-on-windows/<br>

### Running the program
---
After the installation process was executed correcly, navigate to the src folder and open up a terminal in the current folder.
type the following command: ***python PyAlarmClock.py*** .<br>
You should now get the Enter Screen of the application.


#### Optional Arguments
---
There are several optional command line arguments for the program.

1. -c, --camera_num, type=int, default=0 : camera device number for alarm of type open eyes recognition.
2. -e, --ear, type=float, default=0.31 : eye aspect ratio for alarm of type open eyes recognition.
3. -m, --microphone, type=int, default=0 : microphone device number for alarm of type speech recognition.
4. -s, --sim_thresh, type=float, default=0.65 : similarity of words ratio for alarm of type speech recognition.

### Using the Program
---
After running the program through the terminal you will get the following screeen:<br>
![image](https://user-images.githubusercontent.com/37574490/102978850-d7a8fe00-450d-11eb-8560-e37d84a72c1e.png)

#### Adding a TODO task
---
A todo task is a task with a description and date, so the user can track about the tasks he have for a certain day after an alarm is went off.<br><br>
To add a TODO click "Go to TODO" from the enter screen than click on the "+" sign in the next screen you've got.<br>
![image](https://user-images.githubusercontent.com/37574490/102979585-ee038980-450e-11eb-9c56-4431b86df7f9.png)<br>
Select a date and enter a description than check the "v" sign in the bottom of the screen.<br>
![image](https://user-images.githubusercontent.com/37574490/102979813-433f9b00-450f-11eb-9e42-4a2d47d52c62.png)<br>
You can click on the "X" sign to watch the todo that was added:<br>
![image](https://user-images.githubusercontent.com/37574490/102979936-75e99380-450f-11eb-8ffd-bfb1bc83c0c5.png)<br>
From here you can mark the task as "Closed", delete the task or navigate to the enter screen.

#### Adding an Alarm
---
There are three types of alarms, two of them are requirering the user to do some special task in order to turn the alarm of:<br>
1. None type alarm - regular alarm.
2. Face type alarm - the user enters a time in seconds (between 1 - 300), this represants the amount of time he needs to keep his eyes open in front of the camera in order to turn the alarm off.
3. Speech type alarm - the user enters a number of words (between 1 - 10), this represants the number of words the user needs to pronounce correcly in order to turn the alarm off.

To add an alarm, click "Go to Alarms" from the enter screen. Click the "+" sign in order to add an alarm, You Will receive the following screen:<br>
![image](https://user-images.githubusercontent.com/37574490/102980958-01175900-4511-11eb-88e0-529ff4fea8fb.png)<br>

##### Select time
---
Click the button with the clock sign and select a time for the alarm using the time picker opened.<br>
You use the AM/PM option to choose the part of the day for the time (day/night).

##### Enter description
---
Use the text field underneath the time picker to enter a description. You can leave it empty if you wish.<br>

##### Select days
---
Select the days you wish for the alarm to ring, you need to check all the checkboxes representing these days. You must select at least one day.

##### Select alarm type
---
Check the checkboxes in the bottom of the screen to select an alarm type, you must select one exactly.

1. For alarm of type "Face" enter the staring time in front of the camera in the text field underneath (between 1 - 300).
2. For alarm of type "Speech" enter the number of words to pronounce in the text field underneath (between 1 - 10).

##### Submit alarm
---
Add the alarm with the entered parameters by clicking the "V" sign in the bottom toolbar.<br><br>

You can preview the added alarm in the alarms screen.<br><br>
![image](https://user-images.githubusercontent.com/37574490/102982200-d3cbaa80-4512-11eb-8e20-830431fb4538.png)<br>
Notice that you can Edit or Delete the alarm.

### Dismissing an alarm
---
When an alarm time to ring is up you will get the follwoign screen (If you not currently dismissing another alarm):<br>

![image](https://user-images.githubusercontent.com/37574490/102982421-260ccb80-4513-11eb-9540-b686e076f0d4.png)<br>
Clicking the "dismiss" button will execute different actions per alarm type:<br>

##### Dismiss None type alarm
---
Clicking the "dismiss" button will navigate you to a screen showing the TODO tasks for today if there are any.<br>
If there are no tasks for today, you will be navigated to the alarms screen.

##### Dismiss Face type alarm
---
Clicing the "dismiss" button will open up a window from the camera you've provided to the program.<br>
![image](https://user-images.githubusercontent.com/37574490/102983743-3625aa80-4515-11eb-9f21-5c34da7b73fc.png)<br>
You will need to open your eyes in front of the camera for the amount of type you have provided for the alarm in order to turn it off.<br>
You can also press "q" if you wish to skip this process.<br>

##### Dismiss Speech type alarm
---
Clicking the "dismiss" button will navigate you to the following screen contaning the first word you need to pronunce.
![image](https://user-images.githubusercontent.com/37574490/102983811-4e95c500-4515-11eb-8722-61b65dc2d842.png)<br><br>
The Items of the screen in the follwing order (up to bottom, left to right) are representing the following:<br>
1. The current word you need to pronunce.
2. The current word pronunciation.
3. Button when clicked upon plays an audio with the pronunciation of the current word.
4. Part of speech of the current word.
5. Meaning of the current word.
6. Button for recording you pronunciation of the current word.
<br><br>

Click the "record" button and pronounce the current word. If your pronunciation was close enough, you will be navigated to the next word.<br>
If your pronunciation was'nt close enough, you will get an error message.<br>
You can go to the next word by clicking the left-arrow ("->") button in the bottom toolbar.
