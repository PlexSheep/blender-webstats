"""
Render event handlers module.

Contains all Blender render event handler functions that update the render state.
These handlers are called by Blender during the rendering process.
"""

from typing import Optional, List, Tuple

import bpy.types

from blender_webstats import g_render_state
from blender_webstats.util import log


def register_handlers() -> None:
    """
    Register all render event handlers with Blender.

    Args:
        render_state: RenderState instance to update with render events.
    """

    # Create closures that capture the render_state instance
    def handler_render_init(scene: bpy.types.Scene) -> None:
        """
        Called when rendering starts.

        Args:
            scene: Blender scene being rendered.
        """
        g_render_state.reset()
        g_render_state.update_scene_info(scene)
        g_render_state.set_rendering(True)
        log(f"Render started: {scene.name}")

    def handler_render_pre(scene: bpy.types.Scene) -> None:
        """
        Called before rendering each frame.

        Args:
            scene: Blender scene being rendered.
        """
        frame: int = scene.frame_current
        g_render_state.update_frame(frame)
        log(f"Rendering frame {frame}")

    def handler_render_post(scene: bpy.types.Scene) -> None:
        """
        Called after rendering each frame.

        Args:
            scene: Blender scene being rendered.
        """
        log(f"Frame {scene.frame_current} complete")

    def handler_render_complete(scene: bpy.types.Scene) -> None:
        """
        Called when rendering completes.

        Args:
            scene: Blender scene that was rendered.
        """
        g_render_state.set_rendering(False)
        log("Render complete")

    def handler_render_cancel(scene: bpy.types.Scene) -> None:
        """
        Called when rendering is cancelled.

        Args:
            scene: Blender scene that was being rendered.
        """
        g_render_state.set_rendering(False)
        log("Render cancelled")

    def handler_render_stats(scene: bpy.types.Scene) -> None:
        """
        Called periodically with render statistics.

        Parses the statistics string to extract sample progress for Cycles.

        Args:
            scene: Blender scene being rendered.
        """
        stats: str = (
            scene.render.statistics
        )  # BUG: this field does not exist in the render settings
        g_render_state.update_stats(stats)

        # Try to extract sample information from Cycles stats
        if "Sample" in stats:
            try:
                # Example stats: "Fra:1 Mem:123.45M (Peak 234.56M) | Time:00:12.34 | Sample 45/128"
                parts: List[str] = stats.split("Sample")
                if len(parts) > 1:
                    sample_part: str = parts[1].strip().split()[0]  # Get "45/128"
                    if "/" in sample_part:
                        sample_info: List[str] = sample_part.split("/")
                        current: int = int(sample_info[0])
                        g_render_state.update_sample(current)
            except (ValueError, IndexError):
                pass  # If parsing fails, just skip sample update

    # Store handlers as attributes so we can unregister them later
    handler_render_init._webstats_handler = True  # type: ignore
    handler_render_pre._webstats_handler = True  # type: ignore
    handler_render_post._webstats_handler = True  # type: ignore
    handler_render_complete._webstats_handler = True  # type: ignore
    handler_render_cancel._webstats_handler = True  # type: ignore
    handler_render_stats._webstats_handler = True  # type: ignore

    # Register with Blender
    bpy.app.handlers.render_init.append(handler_render_init)
    bpy.app.handlers.render_pre.append(handler_render_pre)
    bpy.app.handlers.render_post.append(handler_render_post)
    bpy.app.handlers.render_complete.append(handler_render_complete)
    bpy.app.handlers.render_cancel.append(handler_render_cancel)
    bpy.app.handlers.render_stats.append(handler_render_stats)


def unregister_handlers() -> None:
    """
    Unregister all render event handlers from Blender.

    Removes all handlers that were registered by this addon.
    """
    # Remove all handlers with our marker attribute
    for handler_list in [
        bpy.app.handlers.render_init,
        bpy.app.handlers.render_pre,
        bpy.app.handlers.render_post,
        bpy.app.handlers.render_complete,
        bpy.app.handlers.render_cancel,
        bpy.app.handlers.render_stats,
    ]:
        handlers_to_remove: List = [
            h for h in handler_list if hasattr(h, "_webstats_handler")
        ]
        for handler in handlers_to_remove:
            handler_list.remove(handler)
