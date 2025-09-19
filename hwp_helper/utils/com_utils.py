"""
COM utilities for robust COM initialization and cleanup.
"""

import threading
import atexit
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Thread-local storage for COM initialization state
_thread_local = threading.local()

def ensure_com_initialized() -> bool:
    """
    Ensure COM is initialized for the current thread.
    Returns True if COM was successfully initialized, False otherwise.
    """
    try:
        import pythoncom
        
        # Check if COM is already initialized for this thread
        if hasattr(_thread_local, 'com_initialized') and _thread_local.com_initialized:
            return True
            
        # Initialize COM
        pythoncom.CoInitialize()
        _thread_local.com_initialized = True
        
        # Register cleanup for this thread
        atexit.register(cleanup_com)
        
        logger.debug("COM initialized for thread")
        return True
        
    except ImportError as e:
        logger.error(f"Failed to import pythoncom: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize COM: {e}")
        return False

def cleanup_com() -> None:
    """Clean up COM for the current thread."""
    try:
        import pythoncom
        
        if hasattr(_thread_local, 'com_initialized') and _thread_local.com_initialized:
            pythoncom.CoUninitialize()
            _thread_local.com_initialized = False
            logger.debug("COM cleaned up for thread")
            
    except ImportError:
        # pythoncom not available, nothing to clean up
        pass
    except Exception as e:
        logger.error(f"Error during COM cleanup: {e}")

def with_com_initialized(func):
    """
    Decorator to ensure COM is initialized before calling a function.
    """
    def wrapper(*args, **kwargs):
        if ensure_com_initialized():
            return func(*args, **kwargs)
        else:
            raise RuntimeError("Failed to initialize COM")
    return wrapper

class COMContext:
    """Context manager for COM initialization."""
    
    def __init__(self):
        self.was_initialized = False
    
    def __enter__(self):
        self.was_initialized = ensure_com_initialized()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.was_initialized:
            cleanup_com()
