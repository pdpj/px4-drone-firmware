#main.py
import asyncio
from utils.mission_orbit import function1

async def main():
    await function1()

if __name__ == "__main__":
    asyncio.run(main())
