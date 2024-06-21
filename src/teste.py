#teste.py
import asyncio

async def function1():
    print("Function1 is running...")
    await asyncio.sleep(2)  # Simulação de alguma tarefa assíncrona
    print("Function1 has completed.")

async def function2():
    print("Function2 is running...")
    await asyncio.sleep(2)  # Simulação de alguma tarefa assíncrona
    print("Function2 has completed.")

if __name__ == "__main__":
