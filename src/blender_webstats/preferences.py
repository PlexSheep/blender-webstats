"""
Addon preferences module.

Defines the user-configurable settings for the WebStats addon.
"""

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import AddonPreferences, Context, UILayout


class WebStatsPreferences(AddonPreferences):
    """Addon preferences for WebStats configuration."""

    bl_idname: str = __package__ or "ERROR"

    # Network settings
    server_host: StringProperty(  # type: ignore
        name="Host Address",
        description="IP address to bind the web server to (0.0.0.0 for all interfaces, 127.0.0.1 for localhost only)",
        default="127.0.0.1",
    )

    server_port: IntProperty(  # type: ignore
        name="Port",
        description="Port number for the web server",
        default=8080,
        min=1024,
        max=65535,
    )

    auto_start: BoolProperty(  # type: ignore
        name="Auto-start Server",
        description="Automatically start the web server when rendering begins",
        default=False,
    )

    # Post-render actions
    enable_shutdown: BoolProperty(  # type: ignore
        name="Shutdown After Render",
        description="Shutdown the computer when rendering completes",
        default=False,
    )

    enable_notification: BoolProperty(  # type: ignore
        name="Audio Notification",
        description="Play a sound when rendering completes",
        default=True,
    )

    def draw(self, context: Context) -> None:
        """
        Draw the preferences UI.

        Args:
            context: Blender context.
        """
        layout: UILayout = UILayout()

        # Network settings
        box: UILayout = layout.box()
        box.label(text="Network Settings:", icon="NETWORK_DRIVE")
        box.prop(self, "server_host")
        box.prop(self, "server_port")
        box.prop(self, "auto_start")

        # Post-render actions
        box = layout.box()
        box.label(text="Post-Render Actions:", icon="CHECKMARK")
        box.prop(self, "enable_notification")
        box.prop(self, "enable_shutdown")

        if self.enable_shutdown:
            box.label(
                text="WARNING: System will shutdown when render completes!",
                icon="ERROR",
            )
