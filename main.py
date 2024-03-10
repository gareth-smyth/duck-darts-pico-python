import machine
import network
from time import sleep
from src.pin_mappings import pin_mappings
import environment
import asyncio
from lib.microdot import Microdot
from lib.websocket import with_websocket, WebSocket
import json


def connect() -> None:
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(environment.SSID, environment.PASSWORD)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')


try:
    connect()
except KeyboardInterrupt:
    machine.reset()

app = Microdot()

out_pins_nums = [0, 1, 2, 3, 4, 5, 6, 7]
in_pin_nums = [28, 27, 26, 22, 21, 20, 19, 18]
button_pin_nums = [14, 15]

in_pins = []
out_pins = []
button_pins = []

for item in in_pin_nums:
    in_pins.append(machine.Pin(item, machine.Pin.OUT))
for item in out_pins_nums:
    out_pins.append(machine.Pin(item, machine.Pin.IN, machine.Pin.PULL_UP))
for item in button_pin_nums:
    button_pins.append(machine.Pin(item, machine.Pin.IN, machine.Pin.PULL_UP))

sockets: list[WebSocket] = []


def scan_keypad():
    for in_pin_idx in range(8):
        in_pins[in_pin_idx].value(0)
        for out_pin_idx in range(8):
            if out_pins[out_pin_idx].value() == 0:
                in_pins[in_pin_idx].value(1)
                return pin_mappings[out_pin_idx + 1][in_pin_idx + 1]
        in_pins[in_pin_idx].value(1)

    for button_idx in range(2):
        if button_pins[button_idx].value() == 0:
            return {'button': button_idx}


async def print_key():
    key = scan_keypad()
    if key is not None:
        print("Key pressed is:{}".format(key))
        for socket in sockets:
            if socket and not socket.closed:
                await socket.send(json.dumps(key))
        await asyncio.sleep_ms(250)
    await asyncio.sleep_ms(0)


async def do_gpio():
    while True:
        await print_key()


@app.route('/ws')
@with_websocket
async def handle_ws(_, ws):
    global sockets
    sockets.append(ws)
    while not ws.closed:
        await ws.receive()
        await asyncio.sleep_ms(1000)
    print("closing")


asyncio.create_task(do_gpio())
print('Running...')
asyncio.create_task(app.run())
print('end...')
