"""HWP application management."""

from pathlib import Path
import subprocess
import pywintypes
import pythoncom
from time import sleep
from typing import Optional

from hwpapi.core import App, Engines

from ..utils.window_utils import set_forewindow, show_window


class HwpAppManager:
    """Manages HWP application instances and connections."""
    
    def __init__(self, dll_path: str = "bin/FilePathCheckerModuleExample.dll"):
        self.dll_path = dll_path
        self._app: Optional[App] = None
    
    @property
    def app(self) -> Optional[App]:
        """Get the current HWP application instance."""
        return self._app
    
    def get_or_create_app(self) -> App:
        """Get existing app or create a new one if needed."""
        if self._app is None or not self._is_app_valid(self._app):
            self._app = self._create_or_connect_app()
        return self._app
    
    def _is_app_valid(self, app: App) -> bool:
        """Check if the HWP app instance is still valid."""
        # Ensure COM is initialized for this thread
        pythoncom.CoInitialize()
        
        try:
            _ = app.api.PageCount
            return True
        except (pywintypes.com_error, AttributeError):
            return False
    
    def _create_or_connect_app(self) -> App:
        """Create new HWP app or connect to existing one."""
        # Ensure COM is initialized for this thread
        pythoncom.CoInitialize()
        
        try:
            # Try to connect to existing app first
            engines = Engines()
            if engines:
                app = App(dll_path=self.dll_path)
                app.engine = engines[0]
                return app
        except Exception:
            pass
        
        # Start new HWP instance
        self._start_hwp()
        
        # Wait for HWP to start and create app
        while True:
            engines = Engines()
            if engines:
                app = App(dll_path=self.dll_path)
                app.engine = engines[0]
                return app
            sleep(1)
    
    def _start_hwp(self) -> None:
        """Start HWP application."""
        hwp_paths = list(Path(r"C:\Program Files (x86)\HNC").rglob("hwp.exe"))
        if hwp_paths:
            subprocess.Popen(hwp_paths[0])
        else:
            raise FileNotFoundError("HWP executable not found")
    
    def bring_to_foreground(self) -> bool:
        """Bring HWP window to foreground."""
        if self._app:
            set_forewindow(self._app)
            show_window(self._app)
            return True
        return False
    
    def ensure_app_ready(self) -> App:
        """Ensure HWP app is ready and bring to foreground."""
        app = self.get_or_create_app()
        self.bring_to_foreground()
        return app
    
    def cleanup(self) -> None:
        """Clean up COM resources."""
        try:
            if self._app:
                self._app = None
            pythoncom.CoUninitialize()
        except Exception:
            pass  # Ignore cleanup errors
