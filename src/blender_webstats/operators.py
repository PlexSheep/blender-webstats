"""
Operators module.

Contains all Blender operators for user interactions.
"""

from typing import Set, Dict, Any

from bpy.types import Operator, Context

from .util import log, log_divider
from .state import RenderState
from . import g_render_state


class WEBSTATS_OT_start_server(Operator):
    """Start the WebStats web server."""

    bl_idname: str = "webstats.start_server"
    bl_label: str = "Start Server"
    bl_description: str = "Start the web server for remote monitoring"

    def execute(self, context: Context) -> Set[str]:
        """
        Execute the operator.

        Args:
            context: Blender context.

        Returns:
            Set containing operator result status.
        """
        # TODO: Implement HTTP server startup in Phase 2
        self.report({"INFO"}, "Server start not yet implemented")
        return {"FINISHED"}


class WEBSTATS_OT_stop_server(Operator):
    """Stop the WebStats web server."""

    bl_idname: str = "webstats.stop_server"
    bl_label: str = "Stop Server"
    bl_description: str = "Stop the web server"

    def execute(self, context: Context) -> Set[str]:
        """
        Execute the operator.

        Args:
            context: Blender context.

        Returns:
            Set containing operator result status.
        """
        # TODO: Implement HTTP server shutdown in Phase 2
        self.report({"INFO"}, "Server stop not yet implemented")
        return {"FINISHED"}


class WEBSTATS_OT_test_state(Operator):
    """Test operator to display current render state."""

    bl_idname: str = "webstats.test_state"
    bl_label: str = "Show Current State"
    bl_description: str = "Display the current render state (for testing)"

    def execute(self, context: Context) -> Set[str]:
        """
        Execute the operator.

        Args:
            context: Blender context.

        Returns:
            Set containing operator result status.
        """

        state: Dict[str, Any] = g_render_state.get_state()
        log_divider("WebStats Render State")
        for key, value in state.items():
            log(f"{key}: {value}")
        log_divider()
        self.report({"INFO"}, "State printed to console")
        return {"FINISHED"}
