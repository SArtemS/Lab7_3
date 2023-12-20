import asyncio
import signal
from datetime import datetime


class ExitException(Exception):
    pass


def raise_exit_program(*args):
    raise ExitException()


async def loopToShowTime():
    await showTime()


async def showTime():
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(current_time)
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
signal.signal(signal.SIGINT, raise_exit_program)

try:
    loop.run_until_complete(loopToShowTime())
except ExitException:
    pass
finally:
    loop.stop()
    print("Exit the program")
    loop.close()
