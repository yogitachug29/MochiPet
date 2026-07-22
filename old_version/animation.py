from PIL import Image, ImageTk


class Animation:

    def __init__(self, size):

        self.size = size
        self.images = {}

        self.load_images()


    def load(self, path):

        image = Image.open(path).convert("RGBA")

        image = image.resize(
            (self.size, self.size),
            Image.LANCZOS
        )

        return ImageTk.PhotoImage(image)



    def load_images(self):

        self.images["idle"] = self.load(
            "assets/expressions/idle_clean.png"
        )

        self.images["blink"] = self.load(
            "assets/expressions/blink_clean.png"
        )

        self.images["happy"] = self.load(
            "assets/expressions/happy_clean.png"
        )

        self.images["thinking"] = self.load(
            "assets/expressions/thinking_clean.png"
        )

        self.images["sad"] = self.load(
            "assets/expressions/sad_clean.png"
        )

        self.images["surprised"] = self.load(
            "assets/expressions/surprised_clean.png"
        )

        self.images["cheering"] = self.load(
            "assets/expressions/cheering_clean.png"
        )

        self.images["drinking"] = self.load(
            "assets/actions/drinking_clean.png"
        )

        self.images["walk_left"] = self.load(
            "assets/walking/walk_left_clean.png"
        )

        self.images["walk_right"] = self.load(
            "assets/walking/walk_right_clean.png"
        )



    def get(self, name):

        return self.images[name]