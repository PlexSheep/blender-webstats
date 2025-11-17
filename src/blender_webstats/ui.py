"""
UI panels module.

Contains all UI panel definitions for the 3D Viewport sidebar.
"""

from typing import Dict, Any, Optional

import bpy
from bpy.types import Panel, Context, UILayout

from blender_webstats.state import RenderState


class WEBSTATS_PT_main_panel(Panel):
    """WebStats main panel in the 3D viewport sidebar."""

    bl_label: str = "WebStats"
    bl_idname: str = "WEBSTATS_PT_main_panel"
    bl_space_type: str = "VIEW_3D"
    bl_region_type: str = "UI"
    bl_category: str = "WebStats"

    # Class variable to store render state reference
    _render_state: RenderState = None  # type: ignore

    @classmethod
    def set_render_state(cls, render_state: RenderState) -> None:
        """
        Set the render state instance for this panel.

        Args:
            render_state: RenderState instance to use.
        """
        cls._render_state = render_state

    def draw(self, context: Context) -> None:
        """
        Draw the panel UI.

        Args:
            context: Blender context.
        """
        layout: UILayout = self.layout

        # Server control
        box: UILayout = layout.box()
        box.label(text="Server Control:", icon="NETWORK_DRIVE")
        row: UILayout = box.row(align=True)
        row.operator("webstats.start_server", icon="PLAY")
        row.operator("webstats.stop_server", icon="PAUSE")

        # Current state display
        box = layout.box()
        box.label(text="Render Status:", icon="RENDER_ANIMATION")

        if self._render_state is None:
            box.label(text="State not initialized", icon="ERROR")
            return

        state: Dict[str, Any] = self._render_state.get_state()

        is_rendering: bool = state["is_rendering"]
        if is_rendering:
            scene_name: str = state["scene_name"]
            render_engine: str = state["render_engine"]
            current_frame: int = state["current_frame"]
            total_frames: int = state["total_frames"]
            current_sample: int = state["current_sample"]
            total_samples: int = state["total_samples"]
            elapsed_time: Optional[float] = state["elapsed_time"]

            box.label(text=f"Scene: {scene_name}", icon="SCENE_DATA")
            box.label(text=f"Engine: {render_engine}", icon="RESTRICT_RENDER_OFF")
            box.label(text=f"Frame: {current_frame}/{total_frames}")

            if total_samples > 0:
                box.label(text=f"Sample: {current_sample}/{total_samples}")

            if elapsed_time is not None:
                elapsed_min: int = int(elapsed_time // 60)
                elapsed_sec: int = int(elapsed_time % 60)
                box.label(text=f"Elapsed: {elapsed_min:02d}:{elapsed_sec:02d}")
        else:
            box.label(text="Not rendering", icon="CANCEL")

        # Testing
        layout.separator()
        layout.operator("webstats.test_state", icon="INFO")
