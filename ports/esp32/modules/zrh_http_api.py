from microdot_asyncio import Microdot, Response
from zrh_response_json import ZrhResponseJson
from zrh_dht import ZrhDHT
from zrh_8x8_led import ZrhLedBoard
from zrh_lcd import ZrhLcd
from zrh_led_box import ZrhLedBox

Response.default_content_type = 'application/json'
res_json = ZrhResponseJson()
app = Microdot()


@app.post("/cmd")
async def cmd(request):
    params = request.json
    print("params:", params)
    print("params[cmd]:", params['cmd'])
    res_json.success("请求成功")
    return res_json.json()


# Temperature and humidity
# 获取温度和湿度
@app.get("/temperature_humidity")
def getTemperatureHumidityData(request):
    zrh_dht = ZrhDHT()
    data = zrh_dht.get_dht_data()
    res_json.success("成功", {
        "temperature": data[0],
        "humidity": data[1]
    })

    return res_json.json()


@app.get("/on_led")
def get_on_led(request):
    color_str = request.args.get("color")
    zrh_led_board = ZrhLedBoard()
    if color_str != None:
        color_arr = color_str.split(',')
        color = tuple(list(map(int, color_arr)))
        zrh_led_board.on_led(color)
    else:
        zrh_led_board.on_led((100, 100, 100))
    res_json.success("成功")
    return res_json.json()


@app.get("/off_led")
def get_off_led(request):
    zrh_led_board = ZrhLedBoard()
    zrh_led_board.off_led()
    res_json.success("成功")
    return res_json.json()


@app.get("/on_led_line")
def get_off_led(request):
    zrh_led_board = ZrhLedBoard()
    zrh_led_board.on_led_line()
    res_json.success("成功")
    return res_json.json()


@app.get("/off_led_line")
def get_off_led_line(request):
    zrh_led_board = ZrhLedBoard()
    zrh_led_board.off_led_line()
    res_json.success("成功")
    return res_json.json()


@app.get("/on_lcd")
def get_on_lcd(request):
    lcd = ZrhLcd()
    lcd.on_lcd()
    res_json.success("成功")
    return res_json.json()


@app.get("/off_lcd")
def get_off_lcd(request):
    lcd = ZrhLcd()
    lcd.off_lcd()
    res_json.success("成功")
    return res_json.json()


@app.get("/on_led_box")
def get_on_led_box(request):
    zrh_led_box = ZrhLedBox()
    zrh_led_box.on_led_box()
    res_json.success("成功")
    return res_json.json()


@app.get("/off_led_box")
def get_off_led_box(request):
    zrh_led_box = ZrhLedBox()
    zrh_led_box.off_led_box()
    res_json.success("成功")
    return res_json.json()


@app.errorhandler(404)
def not_found(request):
    res_json.error("not found")
    return res_json.json(), 404


async def do_http_api():
    app.run(debug=True, port=80)
