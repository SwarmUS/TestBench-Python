# Python Test Bench for the SwarmUS Platform


## Using the graphical tool

This code repository boasts a graphical tool to visualise the interlocalisation feature. 
To use the tool, you will need one stationary HiveBoard with its BeeBoards and at least one mobile
HiveBoard/BeeBoard assembly.

The stationary BeeBoard must be powered by the barrel connector (**not** by USB). Plug the Micro-USB cable to your 
computer for the serial connection.

Next, start the mobile HiveBoard/BeeBoard assemblies.

To start the tool, start the `main.py` file under `src/visualisation_tool`. By default, the visualisation tool will
use the com port `/dev/ttyACM0`. To edit this value, edit the `COM_PORT` variable in `DataUpdater.py`.

The visualisation tool will open a window with an orange dot at the center, representing the stationary HiveBoard. The 
mobile HiveBoards will show as coloured circles and their position will be updated at regular intervals.

![](img/visualisation_tool.png)