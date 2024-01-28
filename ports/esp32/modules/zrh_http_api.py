from microdot_asyncio import Microdot, Response
from zrh_response_json import ZrhResponseJson
from zrh_led import ZrhLedBoard

Response.default_content_type = 'application/json'
res_json = ZrhResponseJson()
app = Microdot()


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


@app.errorhandler(404)
def not_found(request):
    res_json.error("not found")
    return res_json.json(), 404


async def do_http_api():
    app.run(debug=True, port=80)
