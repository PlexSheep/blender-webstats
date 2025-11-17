"""
Blender WebStats - Remote Render Monitoring Addon

A Blender addon for monitoring rendering status remotely via a web interface.
Designed for hobbyists and independents without rendering farms.
"""

from . import util
from . import state
from . import handlers
from . import preferences
from . import operators
from . import ui
from . import estimate

from blender_webstats.util import log
from typing import Tuple, Type

import bpy

bl_info = {
    "name": "Blender WebStats",
    "author": "Christoph J. Scherr",
    "version": (
        0,
        0,
        1,
    ),  # NOTE: This VERSION needs to be changed whenever we change the VERSION in pyproject.toml
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > WebStats",  # TODO: No idea what this means or if it makes sense
    "description": "Monitor render progress remotely via web interface",
    "warning": "Early development version",
    "doc_url": "https://github.com/PlexSheep/blender-webstats",
    "tracker_url": "https://github.com/PlexSheep/blender-webstats/issues",
    "category": "Render",  # TODO: probably not that descriptive
}


# Global render state instance
g_render_state: state.RenderState = state.RenderState()

# Classes to register
_classes: Tuple[Type, ...] = (
    preferences.WebStatsPreferences,
    operators.WEBSTATS_OT_start_server,
    operators.WEBSTATS_OT_stop_server,
    operators.WEBSTATS_OT_test_state,
    ui.WEBSTATS_PT_main_panel,
)


def register() -> None:
    """Register addon classes and handlers."""
    for cls in _classes:
        bpy.utils.register_class(cls)

    handlers.register_handlers(g_render_state)

    log("Addon registered")


def unregister() -> None:
    """Unregister addon classes and handlers."""
    handlers.unregister_handlers()

    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)

    log("Addon unregistered")


if __name__ == "__main__":
    register()
