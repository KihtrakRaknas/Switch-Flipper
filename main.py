from time import sleep
from servo import Servo
import config
from phew import server, connect_to_wifi
from phew.template import render_template

s1 = Servo(28)
state = False

def connect():
    ssid = config.ssid
    password = config.password
    ip = connect_to_wifi(ssid, password)
    
    print(f'Connected on {ip}')
    return ip


@server.route("/turn", methods=["GET"])
def turn_route(request):
    angle = int(request.query.get("angle", -1))
    s1.goto(round(angle/195*1024))
    

@server.route("/on", methods=["GET"])
def on_route(request):
    global state
    state = True
    s1.goto(round(180/195*1024))
    sleep(.15+.05)
    s1.goto(round(90/195*1024))
    sleep(.15)
    s1.free()
    return "On done", 200, "text/html"


@server.route("/off", methods=["GET"])
def off_route(request):
    global state
    state = False
    s1.goto(round(0/195*1024))
    sleep(.2+.05)
    s1.goto(round(90/195*1024))
    sleep(.2)
    s1.free()
    return "Off done", 200, "text/html"


@server.route("/", methods=["GET"])
def turn_webpage_route(request):
    return render_template("index.html")


@server.route("/state", methods=["GET"])
def state_route(request):
    return str(1 if state else 0), 200, "text/html"


@server.catchall()
def catchall(request):
  return "Not found", 404


try:
    connect()
    server.run()
except KeyboardInterrupt:
    print("Halted by user")
