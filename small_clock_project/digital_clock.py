import tkinter as tk
import time
import random
from datetime import datetime, timedelta


class DigitalClock:
    colors = ['red', 'green', 'blue', 'yellow']

    def __init__(self):
        # instance of Tkinter window
        self.master = tk.Tk()
        self.normal_color = 'black'
        self.color = self.normal_color
        self.alarm_time = None
        self.timer_end_time = None
        self.clock_label = tk.Label(self.master, font=('Poppins', 50, 'bold'), background=self.color, foreground='#f80')

    def settings(self):
        # Label the window to "My Clock"
        self.master.title('My Clock')

    def set_alarm(self, time_str):
        self.alarm_time = datetime.strptime(time_str, '%H:%M:%S')

    def set_timer(self, duration_in_seconds):
        self.timer_end_time = datetime.now() + timedelta(seconds=duration_in_seconds)

    def check_alarm(self):
        if self.alarm_time and datetime.now() >= self.alarm_time:
            print('Alarm!')
            self.flash_color()
            self.alarm_time = None

    def check_timer(self):
        if self.timer_end_time and datetime.now() >= self.timer_end_time:
            print('Timer Done!')
            self.flash_color()
            self.timer_end_time = None

    def flash_color(self):
        flash_color = random.choice(DigitalClock.colors)
        self.clock_label.config(background=flash_color)
        # Reset to normal color after 1 second
        self.master.after(1000, lambda: self.clock_label.config(background=self.normal_color))

    def clock(self):
        # Time calculation
        def count_time(time1=''):
            time2 = time.strftime('%H:%M:%S')
            if time2 != time1:
                time1 = time2
                self.clock_label.config(text=time2)
                self.clock_label.after(200, count_time)

            # Check alarm and timer each second
            self.check_alarm()
            self.check_timer()

        # Create the clock text
        self.clock_label.pack(anchor='center')
        # Clock loop
        count_time()
        tk.mainloop()


if __name__ == '__main__':
    my_clock = DigitalClock()
    my_clock.settings()
    my_clock.set_alarm('12:00:00')  # set alarm to 12:00:00
    my_clock.set_timer(10)  # set timer to 10 seconds
    my_clock.clock()

