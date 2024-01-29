from pynput import keyboard

def on_press(key):
    try:
        print('字母键： {} 被按下'.format(key.char))
    except AttributeError:
        print('特殊键： {} 被按下'.format(key))


def on_release(key):
    print('{} 释放了'.format(key))
    if key == keyboard.Key.esc:
        return False


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener.start()

listener.join()


