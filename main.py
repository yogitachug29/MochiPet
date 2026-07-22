"""
Mochi - Desktop Water Reminder Pet
-----------------------------------
A single, borderless Tkinter window that stays completely hidden until
it's time for a water reminder. Mochi then walks in from the right
edge of the screen, waits for you to log a drink (or snooze), and
walks back off screen - fully hiding again until the next reminder.
"""

import tkinter as tk

import tracker
from animation import Animation
from settings import (
    POPUP_WIDTH,
    POPUP_HEIGHT,
    PET_SIZE,
    REMINDER_INTERVAL,
    SNOOZE_TIME,
)
from user_setup import UserSetupDialog
from snooze_tracker import SnoozeTracker

# Auto-update check on startup
try:
    from updater import start_update_check
    start_update_check()
except ImportError:
    pass  # Updater not available in dev environment

# ================= USER SETUP =================
# Show setup dialog on first run
setup_dialog = UserSetupDialog()
setup_dialog.show_setup()
user_profile = setup_dialog.get_user_profile()
snooze_tracker = SnoozeTracker()

# Default values if setup wasn't completed
if not user_profile:
    user_profile = {
        "name": "Friend",
        "gender": "female",
        "daily_target_ml": 2000
    }

# ================= WINDOW SETUP =================
root = tk.Tk()
root.overrideredirect(True)        # Borderless window (no title bar)
root.attributes("-topmost", True)  # Always stay above other windows

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Vertical position: sits just above the taskbar, fixed for the whole run.
y = screen_height - POPUP_HEIGHT - 40

# Horizontal positions used while walking in/out.
x = screen_width                            # Starting point: off-screen
target_x = screen_width - POPUP_WIDTH - 40  # Resting spot near the right edge

# Use a single transparent color across the window.
transparent_color = "white"
root.configure(bg=transparent_color)
root.wm_attributes("-transparentcolor", transparent_color)

# Keep the window hidden while geometry is prepared to avoid top-left flicker.
root.withdraw()
root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")

# Load every sprite frame once, pre-fitted onto a matching-size canvas
# so switching frames never shifts Mochi's position.
animation = Animation(PET_SIZE, gender=user_profile.get('gender', 'female'))

# ================= UI ELEMENTS =================
# Mochi's sprite, centered horizontally in the window.
# Position Mochi slightly lower so her legs can remain near the taskbar,
# while giving enough space above for the speech bubble.
label = tk.Label(root, image=animation.get("idle"), bg=transparent_color, bd=0)
label.place(relx=0.5, y=100, anchor="n")

# ================= SPEECH BUBBLE =================

bubble = None
bubble_canvas = None
bubble_text_id = None
idle_prompt_job = None
busy_prompt_job = None


# ================= BUTTONS =================

# Buttons are created after handler definitions so callbacks exist before assignment.

def get_bubble_font_size(text):
    """Chooses a font size that fits the bubble based on text length."""
    length = len(text)
    if length >= 34:
        return 8
    if length >= 24:
        return 9
    if length >= 16:
        return 10
    return 11


def show_water_bubble(text="💧 Water Time"):
    """Shows Mochi's speech bubble."""

    global bubble, bubble_canvas, bubble_text_id

    if bubble:
        bubble.destroy()

    bubble = tk.Toplevel(root)
    bubble.overrideredirect(True)
    bubble.attributes("-topmost", True)

    bubble_bg = "white"
    bubble.configure(bg=bubble_bg)
    bubble.wm_attributes("-transparentcolor", bubble_bg)

    canvas = tk.Canvas(
        bubble,
        width=230,
        height=120,
        bg=bubble_bg,
        highlightthickness=0
    )
    canvas.pack()

    # Speech bubble
    canvas.create_oval(
        10, 5, 220, 85,
        fill="#FFF4D6",
        outline="#F5CBA7",
        width=2
    )

    # Tail pointing towards Mochi
    canvas.create_polygon(
        140, 85,
        165, 85,
        155, 105,
        fill="#FFF4D6",
        outline="#F5CBA7"
    )

    bubble_text_id = canvas.create_text(
        115,
        40,
        text=text,
        font=("Arial", get_bubble_font_size(text), "bold"),
        fill="#5D4037",
        width=180,
        justify="center"
    )
    bubble_canvas = canvas

    # Bubble near Mochi's face
    bubble.geometry(
        f"+{x+10}+{y+10}"
    )


def update_water_bubble(text):
    """Updates the current speech bubble text if the bubble exists."""
    global bubble, bubble_canvas, bubble_text_id

    if bubble and bubble_canvas is not None and bubble_text_id is not None:
        bubble_canvas.itemconfig(bubble_text_id, text=text)
    else:
        show_water_bubble(text)


def hide_water_bubble():
    """Hides Mochi's speech bubble."""

    global bubble, bubble_canvas, bubble_text_id

    if bubble:
        bubble.destroy()
        bubble = None
    bubble_canvas = None
    bubble_text_id = None




# ================= HELPERS =================
def show_buttons():
    """Reveals the action buttons under Mochi."""
    button_frame.place(relx=0.5, y=220, anchor="n")


def hide_buttons():
    """Hides the action buttons."""
    button_frame.place_forget()


def cancel_idle_prompt():
    """Cancels any pending idle prompt timers."""
    global idle_prompt_job, busy_prompt_job
    if idle_prompt_job is not None:
        root.after_cancel(idle_prompt_job)
        idle_prompt_job = None
    if busy_prompt_job is not None:
        root.after_cancel(busy_prompt_job)
        busy_prompt_job = None


def start_idle_prompt_timer():
    """Starts the first 1-minute idle prompt timer after the pet arrives."""
    cancel_idle_prompt()
    global idle_prompt_job
    idle_prompt_job = root.after(60_000, handle_idle_timeout)


def handle_idle_timeout():
    """Shows the thinking prompt after 1 minute of inactivity."""
    global idle_prompt_job, busy_prompt_job
    idle_prompt_job = None
    update_water_bubble("Are you drinking?")
    label.config(image=animation.get("thinking"))
    busy_prompt_job = root.after(60_000, handle_busy_timeout)


def handle_busy_timeout():
    """Shows the busy message for 7 seconds and then leaves."""
    global busy_prompt_job
    busy_prompt_job = None
    update_water_bubble("I guess you're busy. I'll be back in 5 mins")
    label.config(image=animation.get("idle"))
    root.after(7_000, lambda: handle_snooze(auto=True))


# ================= BUTTON ACTIONS =================
def handle_drink():
    print("DRINK BUTTON CLICKED")

    cancel_reminder()
    cancel_idle_prompt()
    hide_buttons()
    hide_floating_snooze_button()
    show_water_bubble(text="Ahh, Feeling good !!")
    label.config(image=animation.get("drinking"))

    tracker.add_water(250)
    snooze_tracker.reset_snoozed_status()  # Reset snooze count after drinking

    root.after(1500, play_cheer)


def play_cheer():
    """Shows a short farewell before Mochi leaves."""
    show_water_bubble(text="See you after 30 mins !!")
    label.config(image=animation.get("cheering"))
    root.after(2000, play_goodbye)


def play_goodbye():
    """Shows the waving goodbye expression for a moment before leaving."""
    label.config(image=animation.get("happy"))
    root.after(7000, leave_after_drink)


def leave_after_drink():
    """Leaves after celebrating and schedules the next reminder after 30 minutes."""
    leave()
    interval_ms = int(30 * 60 * 1000)
    schedule_reminder(interval_ms)


def handle_snooze(auto=False):
    """Walks Mochi away immediately and reschedules the next reminder."""
    snooze_count = snooze_tracker.increment_snooze()
    
    # If this is the 3rd snooze (index 2), show warning message and lock snooze
    if snooze_tracker.is_snooze_locked() and not auto:
        update_water_bubble("I am not going till you drink water now! 💧")
        show_floating_snooze_button()
        return
    
    cancel_reminder()
    cancel_idle_prompt()
    leave()

    if auto:
        snooze_ms = int(REMINDER_INTERVAL * 60 * 1000)
    else:
        snooze_ms = int(SNOOZE_TIME * 60 * 1000)
    schedule_reminder(snooze_ms)


floating_snooze_window = None

def show_floating_snooze_button():
    """Shows a floating (non-functional) snooze button with message"""
    global floating_snooze_window
    
    if floating_snooze_window:
        return
    
    floating_snooze_window = tk.Toplevel(root)
    floating_snooze_window.overrideredirect(True)
    floating_snooze_window.attributes("-topmost", True)
    floating_snooze_window.configure(bg="white")
    
    # Create a button that's visible but doesn't do anything
    floating_button = tk.Label(
        floating_snooze_window,
        text="😴 Snooze",
        font=("Arial", 9, "bold"),
        bg="#FBEEE6",
        fg="#A04000",
        relief="ridge",
        padx=15,
        pady=6
    )
    floating_button.pack()
    
    # Position the button near the original snooze button
    x_pos = x + 100
    y_pos = y + 240
    floating_snooze_window.geometry(f"+{x_pos}+{y_pos}")
    
    # Make it float around
    float_animation = [0]
    def float_button():
        angle = float_animation[0]
        offset_y = int(10 * __import__('math').sin(angle))
        float_animation[0] += 0.1
        
        floating_snooze_window.geometry(f"+{x_pos}+{y_pos + offset_y}")
        floating_snooze_window.after(50, float_button)
    
    float_button()


def hide_floating_snooze_button():
    """Hides the floating snooze button"""
    global floating_snooze_window
    if floating_snooze_window:
        floating_snooze_window.destroy()
        floating_snooze_window = None


# Buttons are created after handler definitions so callbacks exist before assignment.
button_frame = tk.Frame(
    root,
    bg=transparent_color,
    bd=0
)

drink_button = tk.Button(
    button_frame,
    text="💧 I Drank",
    font=("Arial", 9, "bold"),
    bg="#D6EAF8",
    fg="#154360",
    activebackground="#AED6F1",
    activeforeground="#154360",
    bd=0,
    relief="flat",
    padx=15,
    pady=6,
    cursor="hand2",
    command=handle_drink,
)

drink_button.pack(side="left", padx=6)

snooze_button = tk.Button(
    button_frame,
    text="😴 Snooze",
    font=("Arial", 9, "bold"),
    bg="#FBEEE6",
    fg="#A04000",
    activebackground="#FADBD8",
    activeforeground="#A04000",
    bd=0,
    relief="flat",
    padx=15,
    pady=6,
    cursor="hand2",
    command=handle_snooze,
)

snooze_button.pack(side="left", padx=6)


# ================= SCHEDULING HELPERS =================
reminder_job = None


def cancel_reminder():
    """Cancels any pending reminder callback."""
    global reminder_job
    if reminder_job is not None:
        root.after_cancel(reminder_job)
        reminder_job = None


def schedule_reminder(delay_ms):
    """Schedules the next reminder after a fixed delay."""
    global reminder_job
    cancel_reminder()
    reminder_job = root.after(delay_ms, reminder_loop)


# ================= WALK ANIMATION =================
MOVE_SPEED = 2     # Pixels moved per animation step
REFRESH_RATE = 15  # Milliseconds between animation steps


def walk_in():
    """Slides the window in from the right until it reaches target_x."""
    global x

    x -= MOVE_SPEED
    root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")

    if x <= target_x:
        x = target_x
        root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")
        label.config(image=animation.get("idle"))  # Arrived: face front
        # Personalized message with user's name
        personalized_message = f"💧 {user_profile['name']}, time for some water!"
        show_water_bubble(text=personalized_message)
        show_buttons()
        start_idle_prompt_timer()
        return
    root.after(REFRESH_RATE, walk_in)


def leave():
    """Slides the window off screen to the right, then hides it."""
    global x

    cancel_idle_prompt()
    hide_buttons()
    hide_water_bubble()
    label.config(image=animation.get("walk_right"))

    x += MOVE_SPEED
    root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")

    if x >= screen_width:
        root.withdraw()  # Fully hide the window - nothing left on screen
        return

    root.after(REFRESH_RATE, leave)


def show_pet():
    """Brings the window back and starts the walk-in animation."""
    global x

    tracker.reset_if_new_day()
    cancel_idle_prompt()

    root.deiconify()
    x = screen_width
    root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")
    label.config(image=animation.get("walk_left"))  # Facing left while entering
    walk_in()


# ================= REMINDER SCHEDULER =================
def reminder_loop():
    """Shows Mochi, then reschedules the next reminder."""
    hide_floating_snooze_button()
    show_pet()
    interval_ms = int(REMINDER_INTERVAL * 60 * 1000)
    schedule_reminder(interval_ms)


# ================= START =================
root.withdraw()  # Nothing visible until the first reminder fires

first_interval_ms = int(1 * 60 * 1000)  # start 1 minute after laptop open
schedule_reminder(first_interval_ms)

root.mainloop()