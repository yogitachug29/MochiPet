import json
import datetime


class WaterPet:

    def __init__(self, name="Mochi", daily_goal=5.0):

        self.name = name
        self.daily_goal = daily_goal  # litres
        self.file = "data.json"

        self.water_drunk = 0.0

        self.load_data()


    def load_data(self):

        try:
            with open(self.file, "r") as f:
                data = json.load(f)

            today = str(datetime.date.today())

            if data["date"] == today:
                self.water_drunk = data["water"]

            else:
                self.water_drunk = 0.0
                self.save_data()

        except:
            self.water_drunk = 0.0
            self.save_data()



    def save_data(self):

        data = {
            "date": str(datetime.date.today()),
            "water": self.water_drunk
        }

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)



    def drink_water(self, amount=0.25):

        self.water_drunk += amount


        if self.water_drunk > self.daily_goal:
            self.water_drunk = self.daily_goal


        self.save_data()

        return self.message()



    def remaining(self):

        return round(
            self.daily_goal - self.water_drunk,
            2
        )



    def progress(self):

        return round(
            (self.water_drunk / self.daily_goal) * 100,
            1
        )



    def message(self):

        if self.water_drunk >= self.daily_goal:
            return "Yay! I am fully hydrated 🎉"

        elif self.remaining() <= 1:
            return "Almost done! Drink more 💙"

        else:
            return "I need water 🥺"