import subprocess
import os
import socket

BASE_DIR = r"C:\Loyiha 2026\Instamarket"
VENV_PYTHON = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")

server_process = None


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def start_server():
    global server_process

    if server_process is not None and server_process.poll() is None:
        print("Server allaqachon ishlab turibdi.")
        print("Brauzerda oching: http://127.0.0.1:8000/")
        return

    if not os.path.exists(VENV_PYTHON):
        print("Xatolik: virtual muhit topilmadi.")
        print(f"Tekshirib ko'ring: {VENV_PYTHON}")
        return

    if not os.path.exists(os.path.join(BASE_DIR, "manage.py")):
        print("Xatolik: manage.py topilmadi.")
        print(f"Tekshirib ko'ring: {BASE_DIR}")
        return

    print("Instamarket server ishga tushmoqda...")

    server_process = subprocess.Popen(
        [VENV_PYTHON, "manage.py", "runserver", "0.0.0.0:8000"],
        cwd=BASE_DIR
    )

    local_ip = get_local_ip()

    print("\nServer yoqildi.")
    print("Kompyuterda ochish:")
    print("http://127.0.0.1:8000/")
    print("\nTelefonda ochish:")
    print(f"http://{local_ip}:8000/")


def stop_server():
    global server_process

    if server_process is not None and server_process.poll() is None:
        server_process.terminate()
        server_process.wait()
        print("Server to'xtatildi.")
    else:
        print("Server ishlab turgani yo'q.")


while True:
    print("\n==== INSTAMARKET SERVER BOSHQARUVI ====")
    print("1 - Serverni yoqish")
    print("2 - Serverni o'chirish")
    print("3 - Chiqish")

    choice = input("Tanlang: ").strip()

    if choice == "1":
        start_server()
    elif choice == "2":
        stop_server()
    elif choice == "3":
        stop_server()
        print("Dastur yopildi.")
        break
    else:
        print("Noto'g'ri tanlov.")