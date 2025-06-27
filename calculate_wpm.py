class WPMCalculator:
    def calculate(self, typed_text, time_elapsed):
        words = len(typed_text) / 5
        return round(words / (time_elapsed / 60)) if time_elapsed > 0 else 0