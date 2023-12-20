import asyncio
from datetime import datetime
from pynput import keyboard
from termcolor import colored


async def loopToShowTime():
    with keyboard.Listener(on_release=on_release) as listener:
        await showTime()
        listener.join()


async def showTime():
    while True:
        current_time = colored(datetime.now().strftime("%Y-%b-%d %H:%M:%S"),
                               "red", "on_yellow")
        print(current_time, end="\r")
        await asyncio.sleep(1)


def on_release(key):
    if key == keyboard.Key.esc:
        loop.stop()
        print("\nExit the program")
        return False


loop = asyncio.get_event_loop()
loop.create_task(loopToShowTime())
loop.run_forever()
