import asyncio
import machine
import time
# 定义 GPIO 引脚
button_pin = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)


async def listen_button():
    print("开始监听按钮")
    while True:
        if not button_pin.value():  # 如果按钮被按下，则返回低电平
            print("Button pressed")
            time.sleep_ms(500)  # 防止抖动
        await asyncio.sleep(1)


def run_listen_button():
    asyncio.create_task(listen_button())
