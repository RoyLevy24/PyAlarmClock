# PyAlarmClock

Welcome to PyAlarmClock<br><br>This is a python based alarm clock that uses face and speech recognition in order to turn of alarms.

### Installation
---
1. Make sure you have python 3.6 version or above.
2. Clone this repository.
3. Navigate to the main folder contaning requirements.txt (PyAlarmClock).
4. Open up a terminal in the current folder.
5. First, install cmake using pip by typing the following command: ***pip install cmake==3.18.4.post1***
6. Second, install all the requirements using pip by typing the following command: pip install -r requirements.txt

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
A todo task is a task with a description and date, so the user can track about the tasks he have for a certain day after an alarm is went off.<br><br>
To add a TODO click "Go to TODO" from the enter screen than click on the "+" sign in the next screen you've got.<br>
![image](https://user-images.githubusercontent.com/37574490/102979585-ee038980-450e-11eb-9c56-4431b86df7f9.png)<br>
Select a date and enter a description than check the "v" sign in the bottom of the screen.<br>
![image](https://user-images.githubusercontent.com/37574490/102979813-433f9b00-450f-11eb-9e42-4a2d47d52c62.png)<br>
You can click on the "X" sign to watch the todo that was added:<br>
![image](https://user-images.githubusercontent.com/37574490/102979936-75e99380-450f-11eb-8ffd-bfb1bc83c0c5.png)<br>
From here you can mark the task as "Closed", delete the task or navigate to the enter screen.

#### Adding an Alarm






