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
        self.np.fill(color)
        self.np.write()

    def off_led(self):
        print("self.task:", self.task)
        if self.task is not None:
            print("检查到任务...")
            self.off_led_line()
        self.np.fill((0, 0, 0))
        self.np.write()

    # 生成随机的RGB颜色

    def random_color(self):
        red = random.randint(10, 255)
        green = random.randint(10, 255)
        blue = random.randint(10, 255)
        return (red, green, blue)

    async def run_line(self):
        runs = [0, 1, 2]
        self.np[runs[0]] = (self.random_color())
        self.np[runs[1]] = (self.random_color())
        self.np[runs[2]] = (self.random_color())
        self.np.write()

        while True:
            await asyncio.sleep(0.1)
            # 最后一个灯关闭
            self.np[runs[0]] = ((0, 0, 0))
            self.np.write()

            # 删除最后一个灯
            runs.remove(runs[0])

            # 在前面添加一个灯
            runs.append((runs[-1]+1) % self.num_leds)
            self.np[runs[-1]] = ((self.random_color()))
            self.np.write()

    def on_led_line(self):
        self.task = asyncio.create_task(self.run_line())

    def off_led_line(self):
        self.task.cancel()
        self.np.fill((0, 0, 0))
        self.np.write()
