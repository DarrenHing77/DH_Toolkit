import bpy
import blf

class TextOverlay:
    def __init__(self, text="", position="BOTTOM_CENTER", size=48, color=(1, 1, 1, 1), outline=True):
        self.text = text
        self.position = position  # "BOTTOM_CENTER", "TOP_CENTER", "CENTER", etc.
        self.size = size
        self.color = color
        self.outline = outline
        self._handler = None

    def draw(self):
        """Draw text overlay in all 3D viewports"""
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        self._draw_in_region(region)
                        break
                break

    def _draw_in_region(self, region):
        font_id = 0
        blf.size(font_id, self.size)
        
        # Get text dimensions
        text_width, text_height = blf.dimensions(font_id, self.text)
        
        # Calculate position based on position string
        x, y = self._get_position(region, text_width, text_height)
        
        # Draw outline if enabled
        if self.outline:
            blf.color(font_id, 0.0, 0.0, 0.0, 1.0)
            for dx in [-2, 0, 2]:
                for dy in [-2, 0, 2]:
                    if dx != 0 or dy != 0:
                        blf.position(font_id, x + dx, y + dy, 0)
                        blf.draw(font_id, self.text)
        
        # Draw main text
        blf.color(font_id, *self.color)
        blf.position(font_id, x, y, 0)
        blf.draw(font_id, self.text)

    def _get_position(self, region, text_width, text_height):
        """Calculate text position based on position string"""
        positions = {
            "BOTTOM_CENTER": ((region.width - text_width) / 2, region.height * 0.12),
            "TOP_CENTER": ((region.width - text_width) / 2, region.height * 0.88),
            "CENTER": ((region.width - text_width) / 2, (region.height - text_height) / 2),
            "BOTTOM_LEFT": (20, region.height * 0.12),
            "BOTTOM_RIGHT": (region.width - text_width - 20, region.height * 0.12),
            "TOP_LEFT": (20, region.height * 0.88),
            "TOP_RIGHT": (region.width - text_width - 20, region.height * 0.88),
        }
        return positions.get(self.position, positions["BOTTOM_CENTER"])

    def setup_handler(self, context=None):
        """Setup draw handler"""
        if not self._handler:
            self._handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw, (), 'WINDOW', 'POST_PIXEL'
            )

    def remove_handler(self):
        """Remove draw handler"""
        if self._handler:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self._handler, 'WINDOW')
            except:
                pass
            self._handler = None

    def update_text(self, new_text):
        """Update text and force redraw"""
        self.text = new_text
        self._force_redraw()

    def _force_redraw(self):
        """Force redraw all 3D viewports"""
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()