# TestBench-Python
This repo is the accumulation of many scripts needed in order to calibrate and validate a new set of Beeboard and Hiveboard.
The python scripts are :
- [ExtractRawData](#extractRawData)
- [Parser](#parser)
- [Send_parameters](#send_parameters)
- [Visualisation](#visualisation)
- [Validate](#validate)

## Installation
Prerequisites:

- [Python 3.x](https://www.python.org/downloads/)
- [Pip](https://pypi.org/project/pip/)

Each script has its own requirements.txt wich permits the installation of the required packages
## Normal Order of operation
Follow this flow chart in order to find which script to run depending on your need:
![](img/calibration_flow)<br />
## ExtractRawData
Requires the [TestBench-Arduino](https://swarmus.github.io/SwarmUS-doc/) code to be installed on the test-bench's Arduino in order to be interfaced.
This script enables the user to extract the raw DW1000 data from the HiveBoard/BeeBoards assembly. The test-bench will turn by a chosen stepping angle and acquire the desired amount of raw data per step.
#### Hardware setup
- Place a BeeBoards assembly in the middle of the test-bench. The 0deg axis of the assembly needs to point in a parallel fashion to the mounted laser pointer. 
- The BeeBoards have to be connected to a HiveBoard mounted to the test-bench using the same cable and ports as labeled on the assembly. If the cables and assembly are note indicated be sure to note wich BeeBoards are used, plugged with wich cables and in wich channel on wich HiveBoard. The calibration will only be valid for this configuration and has to be completly re-performed if any of this component is changed or plugged differently.
- Connect power and communication interface to the HiveBoard.
- Connect a usb cable to the Arduino.
- Connect power to the drive submodule (red = 12&nbsp;V, black = ground)
- To align the receiver with the emmiter, use the laser pointer. Each laser should point to the alignment target of the other laser assembly. This position ensures a 0 degree relative orientation between the two radio setup. 
- The laser mount should be calibrated periodicly to ensure its position and accuracy,
#### Runnning the script
The script can be run from the following file (**insert file path**)

#### Adjustable parameters
`USE_ETHERNET` : If true, the communication with the Hiveboard will be done from the Ethernet port. If false, the UART interface will be used, and the following line must be edited to match the port on wich the Hiveboard is connected.
```python
hb_stream = UsbStream('COM16')
```
The Arduino communicates through UART and the following line must be edited: 
```python
testbench = TurningStation('COM15', 115200)
```
`name` : suffix given to the produced CSV with the raw data.<br />
`stepSize` : number of encoder ticks between each acquisition position.<br />
`num_frames` : number of raw data frames to be acquisitioned at each position.<br />
`destination` : ending position of the acquisition. The used encoder has 2048 tick per turn, 2050 should represent a single complete turn.<br />
The data extracted will be saved upon completion of the acquisition once the destination has been reached. The saved data is found in the `/src/data` folder. Each CSV is timestamped and named using the `name` variable

Once these parameters have been adjusted, the file can be run. The *TurningStation* should turn the amount entered in `step` and than stop for 3-5 seconds for the acquisition period before starting to turn again, repeting this cycle until `destination` has been reached


## Parser
Parses and presents the PDOA values from the previously acquired raw data (from control). The user will be prompted 2 clickable interfaces to firstly offset the data to a common reference and secondly to extract the slopes of each antenna pair.
#### Runnning the script
The script can be run from the following file (**insert file path**)
#### Adjustable parameters
`dataFolderPath` : folder path where the extracted raw data CSV has been save.<br />
`dataName` : name of the file to parse the data from.<br />
`usedPairs` : the antenna pairs to be used. Encoded as follow :<br />
pair 0 = antenna 0 - antenna 1<br />
pair 1 = antenna 0 - antenna 2<br />
pair 2 = antenna 1 - antenna 0<br />
....<br />
pair 5 = antenna 2 - antenna 1<br />
`EXPORT_PDOA` : True will prompt the second set of plots (slopes extraction) and save the calibration result in a **pickle** format
#### Behavioral descrition and user interaction
Upon runnning the script, the first plot to appear will ask the user to select points from wich to offset the whole dataset. The first plot represents a sin, the points selected should then be the very bottom of a sin *parabola* section. Also, to obtain a better estimation of the offset needed, it is possible to select the very bottom of the *parabola*, and a top of this *parabola* that has wrapped over. Many points can be selected, the mean of the *y axis* will be used as the offset. If the sin is not wrapping, no points need to be selected, as no offset needs to be applied. This process has to be repeted for the number of `usedPairs` selected. Here is an exemple of the process.<br />
![](img/ex_offset.png)<br />
A plot of the result will then appear. If all curves are not wrapping, the first step is succesful. Otherwise, the script must be re-run and better points must be selected until all curves do not wrap. <br />

The second set of plots is the extraction of the slopes caracteristics. This set will appear only if the `EXPORT_PDOA` has beed set to `True`. A minimum of two lines, and a maximum of three, must be drawn in order to represent the slopes of the data. To draw a line, clic on two points, preferably the farthest appart. Draw at least one line for the rising part and one line for the falling part. This process has to be repeted for the number of `usedPairs` selected. Here is an exemple of the process.<br />
![](img/ex_lines.png)<br />
The saved data will appear in the `dataFolderPath/angleParameters`. Each antenna pair has its own pickle file. These files will also be refered as the **calibration**.
A validation of these files can be done using the `testRead` function from the `Exporter` class.<br />

## Send_parameters
Communicates to the Hiveboard the slope and caracteristics of the 
antenna pairs. Uses the pickle files created by [Parser](#parser). These files need to be placed in the calibration folder using the `hb_{HIVEBOARD_ID}` notation.<br />
#### Runnning the script
The script can be run from the following file (**insert file path**)
#### Adjustable parameters
`HIVEBOARD_ID` : the identification number of the Hiveboard. Can be found either in the flash memory or written on the RJ45 connector. <br />
`MOUNT_ORIENTATION_OFFSET` : the rotation offest, in degrees, applied to the Beeboard assembly between the Test-bench setup at wich the calibration was made, and the orientation on the robot or final installation.<br />
`USE_ETHERNET` : If true, the communication with the Hiveboard will be done from the Ethernet port. If false, the UART interface will be used, and the following line must be adjusted to match the port on wich the Hiveboard is connected.
```python
hb_stream = UsbStream('COM16')
```
#### Behavioral descrition
When the script is ran, the parameters in the calibration folder will be sent to the connected Hiveboard and saved in the flash memory. Thus, there is no need to re-send the parameters on every boot cycle. The calibration should be performed occasionally to ensure the system reliability.

Communication with the HiveBoard is done using the pheromones submodule. If communication problem occur, ensure that the version used by the script is the same as on the HiveBoard.
## Visualisation
When a calibration has been completly transfered to the correspondant Hiveboard, this tool can be used to manually and visually confirm the effectivness of the calibration. Using a emmiter, the user can move around the calibrated Hiveboard and see a marker representing the emmiter move around.

To use the tool, you will need one stationary HiveBoard with its BeeBoards and at least one mobile
HiveBoard/BeeBoard assembly.

The stationary BeeBoard must be powered by the barrel connector (**not** by USB). Plug the Micro-USB cable to your 
computer for the serial connection.

Next, start the mobile HiveBoard/BeeBoard assemblies.

To start the tool, start the `main.py` file under `src/visualisation_tool`. By default, the visualisation tool will
use the com port `/dev/ttyACM0`. To edit this value, edit the `COM_PORT` variable in `DataUpdater.py`.

The visualisation tool will open a window with an orange dot at the center, representing the stationary HiveBoard. The 
mobile HiveBoards will show as coloured circles and their position will be updated at regular intervals. Specific
neighbors can be hidden by unchecking the 'visible' check box in the table underneath the graph.

![](img/visualisation_tool.png)

Communication with the HiveBoard is done using the pheromones submodule. If communication problem occur, ensure that the version used by the script is the same as on the HiveBoard.
## Validate
This is a method to test the whole angles system of the interlocalisation. Using the exact same hardware setup as the calibration it is possible to extract the angle value result from the whole acquisition, linearisation and certitude algorithm.
#### Runnning the script
The script can be run from the following file (**insert file path**)
#### Adjustable parameters
#### Behavioral descrition
#### Results
Communication with the HiveBoard is done using the pheromones submodule. If communication problem occur, ensure that the version used by the script is the same as on the HiveBoard.