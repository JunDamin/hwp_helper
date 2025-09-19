"""Window management utilities."""

import win32gui as wg
import win32con
import pywintypes
import pythoncom
from win32api import GetMonitorInfo, MonitorFromPoint
from typing import Tuple


def set_forewindow(app) -> bool:
    """Safely bring the HWP window to the foreground."""
    # Ensure COM is initialized for this thread
    pythoncom.CoInitialize()
    
    try:
        hwnd = app.api.XHwpWindows.Active_XHwpWindow.WindowHandle
        
        # First try to show the window if it's minimized
        wg.ShowWindow(hwnd, win32con.SW_RESTORE)
        
        # Try to set foreground window
        result = wg.SetForegroundWindow(hwnd)
        
        # If SetForegroundWindow fails, try alternative methods
        if not result:
            # Try using SetWindowPos to bring window to top
            wg.SetWindowPos(
                hwnd, win32con.HWND_TOP, 0, 0, 0, 0, 
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
            )
            
            # Try BringWindowToTop as a fallback
            wg.BringWindowToTop(hwnd)
            
            # Final attempt: Use SetActiveWindow if the window belongs to current thread
            try:
                wg.SetActiveWindow(hwnd)
            except pywintypes.error:
                pass  # This may fail if window belongs to different thread
        
        return True
        
    except (pywintypes.error, AttributeError) as e:
        # Log the error but don't crash the application
        print(f"Warning: Could not bring HWP window to foreground: {e}")
        return False


def show_window(app) -> bool:
    """Show the HWP window."""
    # Ensure COM is initialized for this thread
    pythoncom.CoInitialize()
    
    try:
        hwnd = app.api.XHwpWindows.Active_XHwpWindow.WindowHandle
        return wg.ShowWindow(hwnd, 1)
    except (pywintypes.error, AttributeError):
        return False


def get_screen_size() -> Tuple[int, int, int, int]:
    """Get screen size and position."""
    x1, y1, x2, y2 = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")
    return x1, y1, x2 - x1, y2 - y1


def get_window_position(hwnd: int) -> Tuple[int, int, int, int]:
    """Get window position and size."""
    rect = wg.GetWindowRect(hwnd)
    x, y = rect[0], rect[1]
    width, height = rect[2] - x, rect[3] - y
    return x, y, width, height


def set_window_position(hwnd: int, x: int, y: int, width: int, height: int) -> None:
    """Set window position and size."""
    wg.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, 0)
