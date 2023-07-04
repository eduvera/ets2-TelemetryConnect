## OBS Euro Truck Simulator 2 Telemetry Connect

This repository contains a script that connects OBS with the [ETS2 Telemetry Server](https://github.com/Funbit/ets2-telemetry-server).
Modifies a Text (GDI+) source with a **specific name** with the telemetry data of the same name.

## Setup
**Supported OBS Version**
* OBS Studio 29.1.3

**Supported OS**
* Windows 11 22H2

**Supported Python Version**
* Python 3.11.2

**Installation**
* Download the .py file in this repository
* Open OBS Studio
* Go to **Tools->Scripts* then press the **Add Script** button
* Navigate to the path where the script is saved
* Configure the default settings

If you have doubts please refer to the [OBS Studio Knowledge Base](https://obsproject.com/kb)

## Usage
1. Install and start the telemetry server.
2. Configure the script settings with the URL of your telemetry server API (eg. **server_ip:server_port**/api/ets2/telemetry).
3. Press the **Refresh** button to connect to the telemetry server.
4. Create a Text(GDI+) source in a scene.
5. Rename the Text(GDI+) with the data from telemetry that you want as ***ETS2-arg1-arg2***. (for example: *ETS2-game-connected*)
6. The script will automatically modify the text of the source with the data from the telemetry in the specified interval.

## Important
The naming convention used by this script follows the JSON structure of the Telemetry Server API to retrieve the data and it is case sensitive.
Please refer to the [Telemetry reference](https://github.com/Funbit/ets2-telemetry-server/blob/master/Telemetry.md).

Not all the data in the telemetry is supported. Some data needs to be processed such as *wear*(float) and *game times*(dates). You are free to modify the script to suit your needs.

**Telemetry data not supported**
* truck.placement
* truck.acceleration
* truck.head
* truck.cabin
* truck.hook
* trailer.placement
* job.deadlineTime
* navigation.estimatedTime
* game.nextRestStopTime
* game.time

**Example:**
If you want to show the city from where you pick up the job, the name of the Text(GDI+) source should be ***'ETS2-job-sourceCity'***

