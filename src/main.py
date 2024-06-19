import asyncio
import sys
from teste import function1, function2

async def main():
    await function1()

async def main2():
    await function2()    

async def wait_loop():
    print("Pressione 'x' para calculo de bateria ou 'y' para missao")
    while True:
        key = await get_keypress()
        if key == 'x':
            await main()
        elif key == 'y':
            await main2()

async def get_keypress():
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, sys.stdin.read, 1)
    key = await future
    return key.strip().lower()

if __name__ == "__main__":
    asyncio.run(wait_loop())
