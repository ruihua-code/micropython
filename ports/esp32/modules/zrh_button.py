import asyncio
import machine
import time
from zrh_led import ZrhLedBoard

# 定义 GPIO 引脚
button_pin = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)


async def listen_button():
    print("开始监听按钮")
    while True:
        if not button_pin.value():  # 如果按钮被按下，则返回低电平
            print("Button pressed")

            zrh_led_board = ZrhLedBoard()
            status = zrh_led_board.get_led_status()
            if status == (0, 0, 0):
                zrh_led_board.on_led((100, 100, 100))
            else:
                zrh_led_board.off_led()
            time.sleep_ms(500)  # 防止抖动
        await asyncio.sleep(1)
        print("run...")


def run_listen_button():
    asyncio.create_task(listen_button())