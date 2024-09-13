import machine
import time
from zrh_led import ZrhLedBoard


def on_start(e):
    print("通过按钮开关...")
    zrh_led_board = ZrhLedBoard()
    status = zrh_led_board.get_led_status()
    if status == (0, 0, 0):
        zrh_led_board.on_led((100, 100, 100))
    else:
        zrh_led_board.off_led()


# 定义button类
class button:
    def __init__(self, pin, callback=None, trigger=machine.Pin.IRQ_RISING, min_ago=200):
        # 构造函数初始化
        # pin: GPIO引脚编号
        # callback: 按钮事件触发时调用的回调函数
        # trigger: 中断触发类型，如IRQ_RISING或IRQ_FALLING
        # min_ago: 去抖动时间间隔，单位为毫秒
        self.callback = callback  # 设置回调函数
        self.min_ago = min_ago  # 设置去抖动时间间隔
        self._next_call = time.ticks_add(
            time.ticks_ms(), self.min_ago)  # 计算下一次调用的时间点

        # 创建并配置Pin对象
        self.pin = machine.Pin(pin, machine.Pin.IN,
                               machine.Pin.PULL_UP)  # 配置引脚为输入模式，启用上拉电阻
        # 配置中断，使用debounce_handler作为中断处理函数
        self.pin.irq(trigger=trigger, handler=self.debounce_handler)

        # 内部状态变量
        self._is_pressed = False  # 标记按钮是否被按下

    def call_callback(self, pin):
        # 调用回调函数
        self._is_pressed = True  # 标记按钮被按下
        if self.callback is not None:  # 如果有回调函数
            self.callback(pin)  # 调用回调函数

    def debounce_handler(self, pin):
        # 中断处理函数，用于去抖动处理
        if time.ticks_diff(time.ticks_ms(), self._next_call) > 0:  # 检查是否超过了去抖动时间间隔
            self._next_call = time.ticks_add(
                time.ticks_ms(), self.min_ago)  # 更新下一次调用的时间点
            self.call_callback(pin)  # 调用call_callback函数

    def value(self):
        # 返回按钮的当前状态
        p = self._is_pressed  # 获取按钮状态
        self._is_pressed = False  # 清除状态标记
        return p  # 返回按钮状态


def run_listen_button():
    button(6, on_start)
