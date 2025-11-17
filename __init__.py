"""
Blender WebStats - Remote Render Monitoring Addon

This is a wrapper to expose the addon from src/blender_webstats/
for direct installation via zip file.
"""

# Import the actual addon module
from .src.blender_webstats import (
    bl_info,
    register,
    unregister,
)

# Re-export for Blender
__all__ = ["bl_info", "register", "unregister"]
