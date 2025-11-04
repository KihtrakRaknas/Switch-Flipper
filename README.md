# Switch Flip



## Video Demo 
#### 1 switch
https://github.com/user-attachments/assets/9f9e994c-2c8e-4874-a161-de7cbf6cea0c

#### 2 switches with 1 Pi
https://github.com/user-attachments/assets/0e0c4168-1cfa-4193-8948-caf15af823f2

This code was written in MicroPython to run on a Raspberry Pi Pico W.

This project allows you to remotely turn any wall switch on or off. It is meant
to work with a SG90 or MG90S Servo motor. This makes it inexpensive to automate
fans/lights in a home. Additionally, the switches can still be manually switched
on or off without interacting with the device. I 3D modeled parts to make
everything work, the parts can be viewed here: 
[https://a360.co/4f9oFwI](https://a360.co/4f9oFwI).

## End points

- `/turn`: Rotates servo to specified angle (with the angle query parameter),
useful for finding the right angles you need.
- `/on`: Turns the switch on. Then moves the device back to the neutral position.
- `/off`: Turns the switch off. Then moves the device back to the neutral position.
- `/state`: Returns a 1 or 0 to represent the state of the switch.

### New end points
The newest update adds the ability to control multiple servo motors with one
Pico. The config file now takes in a list of _servo_ports_. The index of each
servo is the index you use in the endpoints:
- `/<index>/turn`
- `/<index>/on`
- `/<index>/off`
- `/<index>/state`

## Set Up
Create a `config.py` folder using `config.py.template` as a reference.

The recommended way to upload MicroPython code to a Raspberry Pi Pico W is using
Thonny. You can upload the python files in this repo through the tool.
