import tkinter as tk


def show_water_reminder():

    popup = tk.Toplevel()

    # ================= WINDOW SETTINGS =================

    popup.title("Water Reminder")

    WIDTH = 300
    HEIGHT = 150

    popup.geometry(
        f"{WIDTH}x{HEIGHT}"
    )

    popup.resizable(
        False,
        False
    )

    popup.attributes(
        "-topmost",
        True
    )

    # Slight transparency
    popup.attributes(
        "-alpha",
        0.95
    )


    # ================= POSITION =================

    popup.update_idletasks()

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    right_margin = 20
    bottom_margin = 60

    x = screen_width - WIDTH - right_margin
    y = screen_height - HEIGHT - bottom_margin

    popup.geometry(
        f"{WIDTH}x{HEIGHT}+{x}+{y}"
    )


    # ================= DESIGN =================

    popup.configure(
        bg="#ffffff"
    )


    title = tk.Label(
        popup,
        text="💧 Mochi Reminder",
        font=("Arial", 15, "bold"),
        bg="white"
    )

    title.pack(
        pady=(15,5)
    )


    message = tk.Label(
        popup,
        text="Time to drink water!\nStay hydrated 😊",
        font=("Arial", 12),
        bg="white"
    )

    message.pack()


    # ================= BUTTONS =================

    button_frame = tk.Frame(
        popup,
        bg="white"
    )

    button_frame.pack(
        pady=15
    )


    def drank():

        popup.destroy()


    def snooze():

        popup.destroy()


    tk.Button(
        button_frame,
        text="🥤 I Drank",
        command=drank,
        font=("Arial", 10)
    ).pack(
        side="left",
        padx=15
    )


    tk.Button(
        button_frame,
        text="⏰ Snooze",
        command=snooze,
        font=("Arial", 10)
    ).pack(
        side="right",
        padx=15
    )