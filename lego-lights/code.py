import adafruit_aw9523
import asyncio
import board
from random import (
    getrandbits,
    randint,
    random,
    seed,
    uniform
)


# LED driver board setup
led_driver = adafruit_aw9523.AW9523(board.STEMMA_I2C())
led_driver.LED_modes = 0xFFFF
led_driver.directions = 0xFFFF

# Seed random generator
seed(getrandbits(32))

# Constants
ON_BRIGHTNESS = 100

# LED groups
ON = (1, 2, 3, 4, 5, 6)
BLINK = (12, 7, 8, 9, 10, 11)
FLICKER = (13, 14, 15)

# Async functions
async def flicker(pin, min, max, interval):
    while True:
        random_current = randint(min, max)
        for current in range(min, random_current):
            led_driver.set_constant_current(pin, current)
            await asyncio.sleep(interval)
        await asyncio.sleep(uniform(0.0, interval))


async def string_lights(interval, max):
    while True:
        for pin in BLINK:
            for current in range(max):
                led_driver.set_constant_current(pin, current)
                await asyncio.sleep(interval)
        for pin in BLINK:
            for current in range(max):
                led_driver.set_constant_current(pin, max - current)
                await asyncio.sleep(interval)

async def blink(pin, interval):
    while True:
        led_driver.set_constant_current(pin, 0)
        await asyncio.sleep(random() * .8)
        led_driver.set_constant_current(pin, 30)
        await asyncio.sleep(interval)


async def main():
    tasks = [asyncio.create_task(flicker(x, randint(5, 9), randint(12, 17), 0.07)) for x in FLICKER]
    blinks = [asyncio.create_task(blink(x, randint(1, 4))) for x in BLINK]
    await asyncio.gather(*tasks)
    await asyncio.gather(*blinks)


# Main Logic
for pin in ON:
    led_driver.set_constant_current(pin, ON_BRIGHTNESS)

asyncio.run(main())