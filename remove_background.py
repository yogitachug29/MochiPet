from rembg import remove
from PIL import Image
import os


folders = [
    "assets/expressions",
    "assets/actions",
    "assets/walking"
]


for folder in folders:

    for file in os.listdir(folder):

        if file.endswith(".png"):

            input_path = os.path.join(
                folder,
                file
            )

            output_path = os.path.join(
                folder,
                file.replace(
                    ".png",
                    "_clean.png"
                )
            )


            print(
                "Removing:",
                input_path
            )


            img = Image.open(input_path)

            result = remove(img)

            result.save(output_path)


print("All backgrounds removed!")