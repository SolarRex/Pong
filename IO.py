from pynput import keyboard, mouse


class Listener:
    def __init__(
        self,
        keyboard_listener: keyboard.Listener = None,
        mouse_listener: mouse.Listener = None,
    ):
        self.keyboard_listener = keyboard_listener  # keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
        self.mouse_listener = mouse_listener  # mouse.Listener(on_click=on_click)

    def on_start(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()

        # self.keyboard_listener.join()
        # self.mouse_listener.join()

    def on_end(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()


# --- Keyboard event handlers ---
def on_key_press(key):
    try:
        print(f"Key pressed: {key.char}")  # Printable keys
    except AttributeError:
        print(f"Special key pressed: {key}")  # Special keys like shift, ctrl, etc.


def on_key_release(key):
    print(f"Key released: {key}")
    if key == keyboard.Key.esc:  # Stop listener on ESC
        print("Stopping listeners...")
        return False  # Returning False stops the listener


# --- Mouse event handlers ---
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse button {button} pressed at ({x}, {y})")
    else:
        print(f"Mouse button {button} released at ({x}, {y})")


if __name__ == "__main__":
    listeners = Listener(
        keyboard.Listener(on_press=on_key_press, on_release=on_key_release),
        mouse.Listener(on_click=on_click),
    )

    listeners.on_start()
