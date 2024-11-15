from time import sleep
from servo import Servo
import config
from phew import server, connect_to_wifi
from phew.template import render_template

servo_ports = config.servo_ports
servos = [Servo(port) for port in servo_ports]
states = [False for _ in servo_ports]


def connect():
    ssid = config.ssid
    password = config.password
    ip = connect_to_wifi(ssid, password)
    
    print(f'Connected on {ip}')
    return ip


def validate_servo_index(func):
    def wrapper(request, servo_index, *args, **kwargs):
        servo_index = int(servo_index)
        try:
            servo_index = int(servo_index)
        except ValueError:
            servo_index = 0
        if servo_index < 0 or servo_index >= len(servos):
            return "Servo not found", 404, "text/html"
        return func(request, servo_index, *args, **kwargs)
    return wrapper


@server.route("/turn", methods=["GET"])
def turn_route_default(request):
    return turn(0, request)
         
@server.route("/<servo_index>/turn", methods=["GET"])
@validate_servo_index
def turn_route(request, servo_index):
    return turn(servo_index, request)

def turn(servo_index, request):
    try:
        angle = int(request.query.get("angle", -1))
    except ValueError:
        return "Invalid angle value", 400, "text/html"
    servos[servo_index].goto(round(angle/195*1024))
    sleep(1)
    servos[servo_index].free()
    return "Turn done", 200, "text/html"
    
    
@server.route("/on", methods=["GET"])
def on_route_default(request):
    return on(0)

@server.route("/<servo_index>/on", methods=["GET"])
@validate_servo_index
def on_route(request, servo_index):
    return on(servo_index)
    
def on(servo_index):
    global states
    states[servo_index] = True
    servos[servo_index].goto(round(180/195*1024))
    sleep(.15+.2)
    servos[servo_index].goto(round(90/195*1024))
    sleep(.15)
    servos[servo_index].free()
    return "On done", 200, "text/html"


@server.route("/off", methods=["GET"])
def off_route_default(request):
    return off(0)

@server.route("/<servo_index>/off", methods=["GET"])
@validate_servo_index
def off_route(request, servo_index):
    return off(servo_index)

def off(servo_index):
    global states
    states[servo_index] = True
    servos[servo_index].goto(round(0/195*1024))
    sleep(.2+.2)
    servos[servo_index].goto(round(90/195*1024))
    sleep(.2)
    servos[servo_index].free()
    return "Off done", 200, "text/html"


@server.route("/state", methods=["GET"])
def state_route_default(request):
    return state(0)

@server.route("/<servo_index>/state", methods=["GET"])
@validate_servo_index
def state_route(request, servo_index):
    return state(servo_index)

def state(servo_index):
    return str(1 if states[servo_index] else 0), 200, "text/html"


@server.route("/", methods=["GET"])
def turn_webpage_route(request):
    return render_template("index.html", servos=servo_ports)


@server.catchall()
def catchall(request):
  return "Not found", 404


try:
    connect()
    server.run()
except KeyboardInterrupt:
    print("Halted by user")
