import win32gui
import win32con
import win32api
import win32process
import psutil
from time import sleep
import sys

def find_window_for_pid(pid):
    def callback(hwnd, hwnds):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(
        callback,
        hwnds
        )
    return hwnds

PROCNAME = "javaw.exe"
procID = []
procHWND = {}

print("Finding processes..")

for p in psutil.process_iter():
    if p.name() == PROCNAME:
        procID.append(int(p.pid))

print("Getting window handles..")
for p in procID:
    procHWND[p] = find_window_for_pid(p)

if len(procID) > 1:
    print("Found %d windows, which PID is the window you're looking for?"%len(procID))
    for i in range(len(procID)):
        print("[%d] %d"%(i+1,procID[i]))
    x = int(input(">> "))
    hWnd = procHWND[procID[x-1]][0]
else:
    print("Found window, with PID %d" %procID[0])
    hWnd = procHWND[procID[0]][0]

win32api.SendMessage(hWnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, win32api.MAKELONG(0,0))
print("Sent RMouse_Down to window %d, exiting"%procID[0])
sleep(1)
sys.exit()
