# Duck Darts Pico Python

Reads and broadcasts "dart thrown" events on specific models of soft tip dartboard connected to a Raspberry Pi Pico W.

## Hardware
### PI
This code is built to run on a Raspberry Pi Pico W loaded with the MicroPython firmware

`RPI_PICO_W-20240222-v1.22.2.uf2`

from [MicroPython Pico](https://micropython.org/download/RPI_PICO_W/)

### Dartboard
The dartboard used has two sets of ribbon cables which are attached to GPIO pins
as described in the `board-config.json` file.

## Software
The software is made up of two components running asynchronously - the GPIO poller,
and the WebSocket server that broadcasts messages.

### Installing the software on your Pi Pico W
1. First make sure you have the MicroPython firmware installed on your pico,
and the pico connected via USB to your computer.

2. run `poetry install --no-root`

3. run `./scripts/install.sh`

### Connecting to the server
The following code shows a simple example of connecting to the server in JS.  
`See example.html` for a simple client application.

The URL used to connect to the WebSocket server will be 

`ws://<IP_ADDRESS_OF_THE_PI>:5000/ws`

## Software used by this application
* The web server and WebSocket code is taken directly from [microdot](https://github.com/miguelgrinberg/microdot)