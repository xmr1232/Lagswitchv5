import tkinter as tk
import subprocess
import threading
import mouse

REAL_GATEWAY = "192.168.87.1"
FAKE_GATEWAY = "192.168.87.254"

armed = False
holding = False


# ---------- NETWORK ----------
def disable_internet():
    global armed

    subprocess.run(
        f'route delete 0.0.0.0 && route add 0.0.0.0 mask 0.0.0.0 {FAKE_GATEWAY}',
        shell=True
    )

    armed = True
    update_gui("OFF (ARMED)", "red")


def enable_internet():
    global armed

    subprocess.run("route delete 0.0.0.0", shell=True)
    subprocess.run(
        f'route add 0.0.0.0 mask 0.0.0.0 {REAL_GATEWAY}',
        shell=True
    )

    armed = False
    update_gui("ON", "green")


# ---------- GUI UPDATE ----------
def update_gui(text, color):
    status_label.config(text=text, bg=color, fg="white")


# ---------- MOUSE ----------
def on_mouse(event):
    global holding, armed

    # M4 = disable
    if event.button == "x" and event.event_type == "down":
        disable_internet()

    # M5 = enable
    if event.button == "x2" and event.event_type == "down":
        enable_internet()

    # hold left click → enable on release
    if armed and event.button == "left":
        if event.event_type == "down":
            holding = True

        elif event.event_type == "up":
            if holding:
                holding = False
                enable_internet()


# ---------- THREAD ----------
def mouse_thread():
    mouse.hook(on_mouse)
    mouse.wait()


# ---------- GUI ----------
root = tk.Tk()
root.title("Internet Switch Controller")
root.geometry("350x180")

status_label = tk.Label(
    root,
    text="READY",
    font=("Arial", 14),
    width=25,
    height=3,
    bg="gray",
    fg="white"
)
status_label.pack(pady=20)

tk.Button(
    root,
    text="Disable Internet (ARM)",
    command=disable_internet,
    width=25
).pack(pady=5)

tk.Button(
    root,
    text="Enable Internet",
    command=enable_internet,
    width=25
).pack(pady=5)


threading.Thread(target=mouse_thread, daemon=True).start()

root.mainloop()


