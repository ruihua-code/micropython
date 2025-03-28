from machine import Pin
import time
from zrh_led import ZrhLedBoard

button_pin = Pin(6, Pin.IN, Pin.PULL_UP)  # 设置为上拉输入模式

zrh_led_board = ZrhLedBoard()


DEBOUNCE_DELAY_MS = 20  # 去抖延时
DEBOUNCE_COUNT = 5  # 去抖检查次数

debounce_counter = 0  # 用于计数稳定低电平的次数


def handle_interrupt(pin):
    global debounce_counter

    # 每次中断时重置计数器
    debounce_counter = 0

    while debounce_counter < DEBOUNCE_COUNT:
        if pin.value() == 0:
            debounce_counter += 1
            time.sleep_ms(DEBOUNCE_DELAY_MS)
        else:
            # 如果在等待期间引脚返回高电平，则重置计数并退出
            debounce_counter = 0
            break

    if debounce_counter == DEBOUNCE_COUNT:
        print("切换状态")
        # 再次检查状态，确保仍然是低电平
    if pin.value() == 0:
        status = zrh_led_board.get_led_status()
        print("zrh按下:", status)
        if status == (0, 0, 0):
            zrh_led_board.on_led((150, 150, 150))
        else:
            zrh_led_board.off_led()


def run_listen_button():
    button_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)
