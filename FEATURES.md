# MochiPet - New Personalization Features

## First Run Setup

When you first launch MochiPet, you'll be asked to provide:

1. **Your Name** - Used in personalized water reminders
2. **Your Gender** - Determines which pet appearance reminds you (Female or Male version)
3. **Daily Water Intake Target** - Your daily hydration goal in milliliters

This information is saved locally on your computer and can be updated by editing `data.json`.

## Personalized Reminders

Once set up, MochiPet will greet you by name:

- Instead of just "Water Time", you'll hear: **"{Your Name}, time for some water!"**

## Smart Snooze System

MochiPet wants you to stay hydrated! Here's how the snooze system works:

### Snoozes Allowed: 2
- **1st Snooze**: You can snooze normally - MochiPet will remind you in 5 minutes
- **2nd Snooze**: You can snooze again - MochiPet will remind you in 5 minutes

### 3rd Reminder (No More Snoozes!)
- On the 3rd consecutive reminder, if you try to snooze:
  - The snooze button will **float in the air** (unclickable)
  - MochiPet will say: **"I am not going till you drink water now!"**
  - You MUST click **"I Drank"** to drink water
  - After drinking, the snooze count resets

### After Drinking
- The counter resets
- You get 2 snoozes again for the next reminder

## Gender-Specific Pet

Your MochiPet appearance changes based on your selected gender:

- **Female**: Default cute pet design
- **Male**: Alternative pet design

*Note: To add male/female specific assets, create folders named `assets/male/` and `assets/female/` with the same structure as `assets/`.*

---

**Want to change your profile?**

Edit `data.json` directly or wait for the next version where we'll add a settings dialog.

Example `data.json`:
```json
{
    "user_profile": {
        "name": "Your Name",
        "gender": "female",
        "daily_target_ml": 2000
    },
    "snooze_count": 0,
    "date": "2026-07-22",
    "water": 1500
}
```
