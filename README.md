**This software was developed to assist in successfully performing the Second Stage Quick Boost in Armored Core: For Answer.**

![スクリーンショット 2025-01-16 154710](https://github.com/user-attachments/assets/c5643236-af1e-4ac2-b622-3d918529f255)
![スクリーンショット 2025-01-16 154743](https://github.com/user-attachments/assets/31277fbc-10e8-4b71-a123-9335da337144)
![スクリーンショット 2025-01-16 164610](https://github.com/user-attachments/assets/a5df1b12-5ec0-48c8-a86f-c1c4d84311e1)

# How to Use
First, the Settings screen will appear. After configuring the necessary items on the Settings screen, press Start, and a meter indicating Sensitivity will be displayed. Practice SS by referring to the sensitivity meter.

## Settings
### Select Joystick
This is the section for selecting a joystick. Please use the same device that you normally use for gaming. If it does not appear in the list, try reconnecting the device and then reloading.
### Select Axis
This is the section for selecting an Axis. Normally, the Axis for the R2 trigger is set to 5. Start by trying 5, and if the behavior seems incorrect, try a different Axis.
### Mode
This is the section for selecting the Mode. There are two options: Window Mode and Overlay Mode. In Window Mode, the Sensitivity meter is displayed as a regular window. In Overlay Mode, it appears on top of other windows, functioning seamlessly even when overlapping with the game.
### Threshold
This is the section for selecting the Threshold. This value adjusts the trigger meter to the optimal position. Please use the same value that is set in RPCS3. If you're using global settings, it can be found in the following directory: 
```
EMULATOR/config/input_configs/global/Default.yml 
```
To easily succeed Second Stage, **it is strongly recommended to set the Threshold value to 0 in RPCS3**.
## UI explanation
### Sensitivity Meter
Rectangle bar displays the trigger pressure. When the meter is yellow, the Second Stage charge count becomes active.
### Charge timer
The circle at the bottom center indicates the duration of the charge count. When edge of the circle turns red, the Second Stage can be successfully executed.
### Notes
By pressing the "s" button while the window is active, you can return to the settings screen. If the overlay option is enabled, you can activate the window by clicking the circle of the charge timer.
# Practice Method for SS
Hold the trigger when the bar turns yellow. The edge of the circle at the bottom will start to move. When the edge of the circle turns red, press the trigger all the way down.\
This software is like training wheels. When attempting advanced gameplay, especially in PvP, you won’t have the luxury of watching the meter. Therefore, you need to practice in test mode or offline missions. Ultimately, you must master SS without relying on the meter.
You need to familiarize yourself with the pressure on the R2 trigger. **It's crucial to sense the pressure with your fingertips.**
# Releases
[Latest - 0.9.7](https://github.com/BEZEL-fA/Visible2ndStage/releases/tag/0.9.7)\
Version 0.9.7 is a version that allows the use of the overlay option.\
[Stable - 0.9.6](https://github.com/BEZEL-fA/Visible2ndStage/releases/tag/0.9.6)\
Version 0.9.6 is a stable version with minimal functionality available.
# Known Issues
It does not support QB reload.\
The required hold time may be slightly inaccurate. The current hold time is between 0.2 to 0.366 seconds.\
The file size is very large. There are issues related to Python compilation.
