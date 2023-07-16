import time  # time module that is used for count downs
import threading  # thread module used for keeping track of multiple timers
import tkinter as tk  # tkinter module that is classified as tk, used in for creating user interface
from tkinter import ttk, PhotoImage


class PomodoroTimer:
    def __init__(self):  # initializes all attributes of self's objects
        self.root = (
            tk.Tk()
        )  # displays the root window and manages all the other components of the tkinter app
        self.root.geometry("600x300")  # dimensions of window
        self.root.title("Pomodoro Timer dmochoco")  # title of window
        self.root.tk.call(
            "wm", "iconphoto", self.root._w, PhotoImage(file="tomato.png")
        )  # adds tomato.png as an icon for window

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 16))
        self.s.configure("TButton", font=("Ubuntu", 16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        # create tabs that will go to different timers
        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = ttk.Label(
            self.tab1, text="25:00", font=("Ubuntu", 48) # create label that shows pomodoro timer 
        )
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = ttk.Label(
            self.tab2, text="05:00", font=("Ubuntu", 48) # create label that shows short break timer 
        )
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = ttk.Label(
            self.tab3, text="15:00", font=("Ubuntu", 48) # create label that shows long break timer 
        )
        self.long_break_timer_label.pack(pady=20)

        # name the tabs for each of the respective timers
        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        # create start button
        self.start_button = ttk.Button(
            self.grid_layout, text="Start", command=self.start_timer_thread 
        )
        self.start_button.grid(row=0, column=0)

        # create skip button
        self.skip_button = ttk.Button(
            self.grid_layout, text="Skip", command=self.skip_clock
        )
        self.skip_button.grid(row=0, column=1)

        # create reset button
        self.reset_button = ttk.Button(
            self.grid_layout, text="Reset", command=self.reset_clock
        )
        self.reset_button.grid(row=0, column=2)

        # create label that displays amount of pomodoros collected
        self.pomodoro_counter_label = ttk.Label(
            self.grid_layout, text="Pomodoros: 0", font=("Ubuntu", 16)
        )
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.pomodoros = 0 # pomodoro counter variable 
        self.skipped = False # bool variable to see if timer has been skipped 
        self.stopped = False # bool variable to see if timer has been stopped 
        self.running = False # bool variable to see if timer is still running 

        self.root.mainloop()  # infinite loop that is used to run the window

    # function that creates new thread for timer
    def start_timer_thread(self):
        if not self.running:  # if timer is currently not running
            t = threading.Thread(target=self.start_timer)
            t.start()  # start new thread
            self.running = True  # timer is now running

    # function that starts timer
    def start_timer(self):
        self.stopped = False  # timer is not stopped
        self.skipped = False  # timer is not skipped
        timer_id = (
            self.tabs.index(self.tabs.select()) + 1
        )  # timer id variable that indentifies which timer is currently running

        if timer_id == 1:  # POMODORO TIMER 
            full_seconds = 60 * 25  # seconds of the 25 minute timer
            while (
                full_seconds > 0 and not self.stopped # loop while full seconds is still going and timer has not been stopped
            ):  
                minutes, seconds = divmod(
                    full_seconds, 60 # minutes = full_seconds/60, seconds = full_seconds%60
                )  
                self.pomodoro_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}" # label that displays timer counting down
                )  
                self.root.update()
                time.sleep(1) # wait 1 second
                full_seconds -= 1 # decrement seconds 
            if not self.stopped or self.skipped: # if the timer has not stopped or has not been skipped 
                self.pomodoros += 1 # add 1 to pomodoro counter 
                self.pomodoro_counter_label.configure(
                    text=f"Pomodoros: {self.pomodoros}" # print amount of total pomodoros
                )
                if self.pomodoros % 4 == 0: # for every four pomodoros 
                    self.tabs.select(2) # switch to long break
                    self.start_timer() 
                else: 
                    self.tabs.select(1) # switch to short break
                self.start_timer()

        # note* same comments apply to short break and long break timers 
        elif timer_id == 2: # SHORT BREAK TIMER 
            full_seconds = 60 * 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}"
                )
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()

        elif timer_id == 3: # LONG BRAEK TIMER
            full_seconds = 60 * 15
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}"
                )
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        else:
            print("Invalid Timer ID")

    # reset clock function
    def reset_clock(self):
        self.stopped = True  # timer has been stopped
        self.skipped = False  # timer has NOT been skipped
        self.pomodoros = 0  # reset pomodoros back to 0
        self.pomodoro_timer_label.config(text="25:00")  # reset pomo timer to 25 minutes
        self.short_break_timer_label.config(
            text="05:00"
        )  # reset short timer to 5 minutes
        self.long_break_timer_label.config(
            text="15:00"
        )  # reset long timer to 15 minutes
        self.pomodoro_counter_label.config(
            text="Pomodoros: 0"
        )  # reset pomodoros counter to 0
        self.running = False  # timer is NOT currently running

    # skip clock function
    def skip_clock(self):
        current_tab = self.tabs.index(  # current_tab variable is equal to the tab that the window is currently on
            self.tabs.select()
        )
        if (
            current_tab
            == 0  # if on pomodoro tab, start timer back at 25 minutes and countdown
        ):
            self.pomodoro_timer_label.config(text="25:00")
        elif (
            current_tab
            == 1  # if on short break tab, start timer back to 5 minutes and countdown
        ):
            self.short_break_timer_label.config(text="05:00")
        elif (
            current_tab
            == 2  # if on long braek tab, start timer back to 15 minutes and countdown
        ):
            self.long_break_timer_label.config(text="15:00")
        self.stopped = True  # timer has stopped
        self.skipped = True  # timer has been skipped


PomodoroTimer()
