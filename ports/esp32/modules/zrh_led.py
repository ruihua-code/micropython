import neopixel
import machine
import random
import asyncio


class ZrhLedBoard:
    num_leds = 80  # LED矩阵中LED的数量
    # 初始化NeoPixel
    np = neopixel.NeoPixel(machine.Pin(18), num_leds)
    task = None

    def on_led(self, color):
        print("color:", color)
        ZrhLedBoard.np.fill(color)
        ZrhLedBoard.np.write()

    def off_led(self):
        ZrhLedBoard.np.fill((0, 0, 0))
        ZrhLedBoard.np.write()

    # 生成随机的RGB颜色

    def random_color():
        red = random.randint(10, 255)
        green = random.randint(10, 255)
        blue = random.randint(10, 255)
        return (red, green, blue)

    async def run_line():
        runs = [0, 1, 2]
        ZrhLedBoard.np[runs[0]] = (ZrhLedBoard.random_color())
        ZrhLedBoard.np[runs[1]] = (ZrhLedBoard.random_color())
        ZrhLedBoard.np[runs[2]] = (ZrhLedBoard.random_color())
        ZrhLedBoard.np.write()

        while True:
            await asyncio.sleep(0.1)
            # 最后一个灯关闭
            ZrhLedBoard.np[runs[0]] = ((0, 0, 0))
            ZrhLedBoard.np.write()

            # 删除最后一个灯
            runs.remove(runs[0])

            # 在前面添加一个灯
            runs.append((runs[-1]+1) % ZrhLedBoard.num_leds)
            ZrhLedBoard.np[runs[-1]] = ((ZrhLedBoard.random_color()))
            ZrhLedBoard.np.write()

    def on_led_line(self):
        ZrhLedBoard.task = asyncio.create_task(ZrhLedBoard.run_line())

    def off_led_line(self):
        ZrhLedBoard.task.cancel()
        ZrhLedBoard.np.fill((0, 0, 0))
        ZrhLedBoard.np.write()
