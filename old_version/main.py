import tkinter as tk

from animation import Animation
from old_version.water_reminder import show_water_reminder
from pet import WaterPet


# ================= PET DATA =================

pet = WaterPet("Mochi", 5.0)


# ================= WINDOW =================

root = tk.Tk()

root.overrideredirect(True)
root.attributes("-topmost", True)

PET_SIZE = 200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Start outside screen
x = screen_width
y = screen_height - PET_SIZE - 90

# Final position
target_x = screen_width - PET_SIZE - 120

root.geometry(f"{PET_SIZE}x{PET_SIZE}+{x}+{y}")

root.config(bg="white")
root.wm_attributes("-transparentcolor", "white")


# ================= ANIMATION =================

animation = Animation(PET_SIZE)

current_image = "walk_left"

label = tk.Label(
    root,
    image=animation.get(current_image),
    bg="white",
    bd=0
)

label.pack()


# ================= WATER BUTTON =================

def drink():

    global current_image

    message = pet.drink_water(0.25)

    print(message)

    print(
        f"{pet.water_drunk:.2f} L / {pet.daily_goal} L"
    )

    current_image = "drinking"
    label.config(image=animation.get(current_image))

    root.after(1500, happy_animation)


def happy_animation():

    global current_image

    current_image = "cheering"
    label.config(image=animation.get(current_image))

    root.after(2000, idle_animation)


button = tk.Button(
    root,
    text="🥛 I drank",
    command=drink,
    font=("Arial", 9)
)

button.place(
    x=60,
    y=165
)


# ================= IDLE =================

def idle_animation():

    global current_image

    current_image = "idle"

    label.config(
        image=animation.get(current_image)
    )


# ================= BLINK =================

def blink():

    global current_image

    if current_image == "idle":

        label.config(
            image=animation.get("blink")
        )

        root.after(
            250,
            idle_animation
        )

    root.after(
        5000,
        blink
    )


# ================= WALK IN =================

speed = 4


def walk_in():

    global x

    x -= speed

    root.geometry(
        f"{PET_SIZE}x{PET_SIZE}+{x}+{y}"
    )

    if x <= target_x:

        x = target_x

        root.geometry(
            f"{PET_SIZE}x{PET_SIZE}+{x}+{y}"
        )

        idle_animation()

        return

    root.after(
        20,
        walk_in
    )


# ================= DRAG =================

drag_x = 0
drag_y = 0


def start_drag(event):

    global drag_x, drag_y

    drag_x = event.x
    drag_y = event.y


def move_drag(event):

    global x, y

    x = event.x_root - drag_x
    y = event.y_root - drag_y

    root.geometry(
        f"{PET_SIZE}x{PET_SIZE}+{x}+{y}"
    )


label.bind(
    "<Button-1>",
    start_drag
)

label.bind(
    "<B1-Motion>",
    move_drag
)


# ================= REMINDER =================

def reminder_loop():

    show_water_reminder()

    root.after(
        1800000,
        reminder_loop
    )


# ================= START =================

root.after(
    1000,
    walk_in
)

root.after(
    4000,
    blink
)

root.after(
    5000,
    reminder_loop
)

root.mainloop()