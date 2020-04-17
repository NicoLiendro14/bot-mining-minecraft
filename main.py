import pyautogui
import time
import ctypes
import datetime

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def auto_mining(cant_pickaxe, time_mining = 180):
    cant_pickaxe = cant_pickaxe + 3
    for i in range (3,cant_pickaxe):
        now = datetime.datetime.now()
        after = now + datetime.timedelta(seconds=time_mining)
        print("Mining N°"+str(i-1)+" starts at: "+str(now))
        print("This ends at: "+str(after))
        for j in range(1,10):
            time.sleep(5)
            PressKey(0x2a) # W
            PressKey(0x11) # Shift Left

            pyautogui.mouseDown()
            time.sleep(time_mining/10)
            pyautogui.mouseUp() 
            time.sleep(1)

            ReleaseKey(0x2a) # W
            ReleaseKey(0x11) # Shift Left
            time.sleep(1)

            PressKey(0x02) #1
            ReleaseKey(0x02)
            time.sleep(2)

            pyautogui.moveTo(1, 512)
            time.sleep(2)
            pyautogui.click(button='right')
            time.sleep(2)

            pyautogui.moveTo(1280, 512)
            PressKey(0x0+i) 
            ReleaseKey(0x0+i)
    PressKey(0x01) #Esc
    ReleaseKey(0x01)
    

def auto_mining_straight(cant_pickaxe, time_mining = 180):
    for i in range(1,cant_pickaxe):
        time.sleep(5)
        PressKey(0x2a) # W
        PressKey(0x11) # Shift Left

        pyautogui.mouseDown()
        time.sleep(time_mining)
        pyautogui.mouseUp() 
        time.sleep(1)

        ReleaseKey(0x2a) # W
        ReleaseKey(0x11) # Shift Left
        time.sleep(1)
        PressKey(0x0+i) 
        ReleaseKey(0x0+i)
        
def menu(cant_pickaxe):
    while True:
        try:
            print("1- Mining straight with torchs")
            print("2- Mining straight without torchs")
            print("3- Exit")
            value = int(input())
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if value == 1:
            print("Mining straight with torchs...")
            auto_mining(cant_pickaxe)
        if value == 2: 
            print("Mining straight without torchs...")
            auto_mining_straight(cant_pickaxe) 
        if value == 3:
            print("Exiting...")
            break

def menu_pickaxes():
    while True:
        try:
            print("Numbers of pickaxes you will use: (between 1 and 9)")
            value = int(input())
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if value >= 0 and value <= 9:
            return value

if __name__ == "__main__":
    cant_pickaxe = menu_pickaxes()
    menu(cant_pickaxe)   

