import os
import sys
from pathlib import Path

from PIL import Image, ImageTk
from settings import PET_SIZE


def get_resource_path(relative_path):
    """Resolve a file path for both source runs and packaged executables."""
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return str(Path(base_path) / relative_path)


class Animation:
    """
    Loads and prepares every one of Mochi's sprite frames.

    The source PNGs are all different physical sizes (idle is wide and
    short, the walking frames are tall and narrow, drinking is somewhere
    in between). If we just draw them as-is, Mochi visually "jumps"
    every time the sprite changes, because the artwork sits at a
    different position inside each image.

    To fix that properly, every frame goes through the same pipeline:

        1. Crop away the fully-transparent padding around the artwork.
        2. Scale it down, keeping its original aspect ratio, so it fits
           inside a fixed square canvas (self.size x self.size).
        3. Paste it centered onto a transparent canvas of that exact
           size.

    The result: animation.get(...) always returns an image of the same
    width and height, so the Tkinter label never has to be manually
    repositioned when the sprite changes.
    """

    def __init__(self, size=PET_SIZE, gender="female"):
        # Side length (in pixels) of the square canvas every sprite is
        # centered onto.
        self.size = size
        self.gender = gender  # "female" or "male"
        self.images = {}
        self.load_images()

    def _crop_transparent_border(self, image):
        """Crops away fully-transparent padding around the artwork."""
        bbox = image.getbbox()
        if bbox:
            return image.crop(bbox)
        return image

    def _fit_on_canvas(self, image):
        """
        Scales `image` down (preserving aspect ratio) so it fits inside
        a self.size x self.size box, then pastes it centered onto a
        transparent canvas of exactly that size.
        """
        image = self._crop_transparent_border(image)

        # Scale so the longer relevant side fits inside the canvas.
        scale = min(self.size / image.width, self.size / image.height)
        new_width = max(1, int(image.width * scale))
        new_height = max(1, int(image.height * scale))
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Paste the resized artwork centered onto a blank transparent canvas.
        canvas = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        offset_x = (self.size - new_width) // 2
        offset_y = (self.size - new_height) // 2
        canvas.paste(image, (offset_x, offset_y), image)

        return canvas

    def load(self, path):
        """Loads a PNG from disk and returns a canvas-fitted PhotoImage."""
        if not os.path.exists(path):
            print(f"Warning: Asset file not found at {path}")
            return None

        try:
            image = Image.open(path).convert("RGBA")
            canvas = self._fit_on_canvas(image)
            return ImageTk.PhotoImage(canvas)
        except Exception as e:
            print(f"Error loading image path {path}: {e}")
            return None

    def load_images(self):
        """Pre-loads all expressions, actions, and walking frames."""
        # Check if gender-specific assets exist, otherwise use default
        base_path = "assets"
        gender_path = f"assets/{self.gender}" if self.gender != "female" else "assets"
        
        # Try gender-specific path first, fall back to default
        def get_asset_path(filename):
            gender_specific = os.path.join(gender_path, filename)
            if os.path.exists(get_resource_path(gender_specific)):
                return gender_specific
            return os.path.join(base_path, filename)
        
        # Expressions
        self.images["idle"] = self.load(get_resource_path(get_asset_path("expressions/idle_clean.png")))
        self.images["blink"] = self.load(get_resource_path(get_asset_path("expressions/blink_clean.png")))
        self.images["happy"] = self.load(get_resource_path(get_asset_path("expressions/happy_clean.png")))
        self.images["thinking"] = self.load(get_resource_path(get_asset_path("expressions/thinking_clean.png")))
        self.images["sad"] = self.load(get_resource_path(get_asset_path("expressions/sad_clean.png")))
        self.images["surprised"] = self.load(get_resource_path(get_asset_path("expressions/surprised_clean.png")))
        self.images["cheering"] = self.load(get_resource_path(get_asset_path("expressions/cheering_clean.png")))

        # Actions
        self.images["drinking"] = self.load(get_resource_path(get_asset_path("actions/drinking_clean.png")))

        # Walking frames each have their own dedicated artwork, already
        # facing the correct direction, so we load them directly.
        self.images["walk_left"] = self.load(get_resource_path(get_asset_path("walking/walk_left_clean.png")))
        self.images["walk_right"] = self.load(get_resource_path(get_asset_path("walking/walk_right_clean.png")))

    def get(self, name):
        """Safely fetches a cached frame, falling back to idle if missing."""
        return self.images.get(name, self.images.get("idle"))