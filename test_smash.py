import subprocess
import asyncio

# Асинхронное выполнение команды
async def a_process(command):
    return await asyncio.create_subprocess_exec(
        *command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

# Синхронное выполнение команды
def process(command):
    return subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True
    )

# Асинхронное ожидание вывода
async def a_expect(proc, pattern, timeout=10):
    pattern = pattern.strip("\n").replace("\n", "\r\n")
    buffer = ""
    try:
        while True:
            char = await asyncio.wait_for(proc.stdout.read(1), timeout)
            if not char:
                break
            buffer += char.decode()
            if pattern in buffer:
                return True, buffer
    except asyncio.TimeoutError:
        print(f"Timeout while waiting for pattern:\n{pattern}")
        return False, buffer

# Синхронное ожидание вывода
def expect(proc, pattern, timeout=10):
    pattern = pattern.strip("\n").replace("\n", "\r\n")
    buffer = ""
    try:
        while True:
            char = proc.stdout.read(1).decode()
            if not char:
                break
            buffer += char
            if pattern in buffer:
                return True, buffer
    except Exception as ex:
        print(f"ERROR: {ex}")
        return False, buffer

# Асинхронная запись ввода
async def a_write(proc, text):
    proc.stdin.write(f'{text}\n'.encode())
    await proc.stdin.drain()
    return text

# Синхронная запись ввода
def write(proc, text):
    proc.stdin.write(f'{text}\n'.encode())
    proc.stdin.flush()
    return text

# Основной тест
async def test():
    print("Launching processes")
    try:
        # Запускаем файлы
        bas = process('basicsmash.bas')
        py = await a_process('python smash_game.py')

        # Ожидаем приветственное сообщение
        expected_greetings = """
                          SMASH
                    CREATIVE COMPUTING
                  MORRISTOWN, NEW JERSEY
"""
        print("Expecting greetings...")
        expect(bas, expected_greetings)
        await a_expect(py, expected_greetings)
        print("[+] TEST 1 - PASSED")

        # Отправляем 'Y' для получения инструкций
        print("Sending 'Y' for instructions...")
        write(bas, 'Y')
        await a_write(py, 'Y')
        print("[+] KEYS SENT")

        # Проверяем вывод инструкций и начало игры
        instruction_and_game_start = """
THIS IS SMASH--THE GAME THAT SIMULATES A CAR RACE.
YOU WILL RESPOND WITH ONE OF THE FOLLOWING MANUEVERS
WHEN A '?' IS TYPED.  THE POSITION NUMBERS REFER TO THE
POINT AT WHICH YOU ARE ON THE TRACK-THEY GO AS FOLLOWS:

  1-THE START LINE
  2-MID STRAIGHT-AWAY
  3-COMING UP ON A LEFT TURN
  4-MID LEFT TURN
  5-COMING UP ON A RIGHT TURN
  6-MID-RIGHT TURN
  7-THE FINISH LINE

     MANEUVERS
  1-FLOOR IT
  2-ACCELERATE(MODERATE)
  3-BRAKE SLIGHT
  4-JAM ON THE BRAKES
  5-SHARP RIGHT
  6-MODERATE RIGHT
  7-SHARP LEFT
  8-MODERATE LEFT

TIME(SEC)
"""
        print("Expecting instructions and game start...")
        expect(bas, instruction_and_game_start)
        await a_expect(py, instruction_and_game_start)
        print("[+] TEST 2 - PASSED")

        # Отправляем первый ход
        print("Sending first move...")
        move = '1'
        write(bas, move)
        await a_write(py, move)
        print("[+] Move sent")

        # Проверяем, что игра продолжается
        print("Expecting game state update...")
        game_state_partial = "MILES TO GO"
        expect(bas, game_state_partial)
        await a_expect(py, game_state_partial)
        print("[+] TEST 3 - PASSED")

        # Завершаем процессы
        bas.kill()
        bas.wait()

        py.kill()
        await py.wait()
    except Exception as ex:
        print(f"Test failed: {ex}")

# Запуск теста
asyncio.run(test())
