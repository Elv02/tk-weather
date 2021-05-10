"""
    A weather app written in Python using Tkinter.
    Hooks up to (INSERT API CALL HERE).
"""

from tkinter.constants import BOTH, GROOVE, N, RAISED, SUNKEN, LEFT, RIGHT, W, YES
import requests
from tkinter import Button, Entry, Label, LabelFrame, Menu, Radiobutton, StringVar, Tk, Frame, Toplevel, messagebox

from functools import partial

# TODO: VERY IMPORTANT! MOVE/HIDE THIS KEY SOMEWHERE!!!
MY_KEY = "498779c46add2008eac96a53dfa56c64"

MSG_INFO = 0
MSG_WARNING = 1
MSG_ERROR = 2

OK = 0
ERROR = 1

TEMP_C = 0
TEMP_F = 1

NYI = "Not yet implemented!"

class Interface:
    """
        Holds all logic for the front end user interface
    """
    def __init__(self) -> None:
        """
            Construct a new interface instance.
            Sets up all UI elements but does not start main TK look (use launch_interface).
        """
        self.data = ClientData()

        self.init_gui()

    def init_gui(self) -> None:
        """
            Initialize the GUI elements.
        """
        self.root = Tk()
        
        menubar = Menu(self.root)
        self.root.config(menu = menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Weather Data", command=partial(self.show_msg, NYI, MSG_WARNING))
        filemenu.add_command(label="Open New Window", command=partial(self.show_msg, NYI, MSG_WARNING))
        filemenu.add_command(label="Close Current Window", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="General Settings", command=self.change_settings)
        settings_menu.add_command(label="Change City", command=self.change_city)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=partial(self.show_msg, NYI, MSG_WARNING))
        help_menu.add_command(label="Help", command=partial(self.show_msg, NYI, MSG_WARNING))
        menubar.add_cascade(label="Help", menu=help_menu)

        location_frame = Frame(self.root)
        self.city_label = Label(master=location_frame, text="Toronto")
        self.city_label.grid(column=0, row=0)
        self.state_label = Label(master=location_frame, text="Ontario")
        self.state_label.grid(column=0, row=1)
        self.country_label = Label(master=location_frame, text="Canada")
        self.country_label.grid(column=0, row=2)
        self.longitude_label = Label(master=location_frame, text="Longitude: <DEG>")
        self.longitude_label.grid(column=0, row=3)
        self.latitude_label = Label(master=location_frame, text="Latitude: <DEG>")
        self.latitude_label.grid(column=0, row=4)
        location_frame.grid(column=0, row=0)

        current_weather_frame = Frame(self.root)
        self.current_weather_label = Label(master=current_weather_frame, text="<INSERT WEATHER DATA>")
        self.current_weather_label.grid(column=0, row=0)
        self.current_weather_image = Label(master=current_weather_frame, text="<INSERT GRAPHIC HERE>")
        self.current_weather_image.grid(column=1, row=0)
        current_weather_frame.grid(column=1, row=0)

        forecast_weather_frame = Frame(self.root)
        self.forecast_cells = []
        for i in range(7):
            cell = Label(master=forecast_weather_frame, text="<DAY>")
            cell.grid(column=i, row=0)
            self.forecast_cells.append(cell)
        forecast_weather_frame.grid(column=0, row=1, rowspan=2)

        # Hidden elements (new windows)
        self.change_city_label = None
        self.new_city_entry = None
        self.new_state_entry = None
        self.new_country_entry = None

    def launch_interface(self) -> None:
        """
            Launch the interface (starts main tk loop).
        """
        self.root.mainloop()

    def update_interface(self) -> None:
        """
            Get updated info from API and push to interface
        """
        pass

    def change_settings(self) -> None:
        """
            Open a new settings window and get user updated preferences
        """
        settings_window = Toplevel(self.root)
        temp_frame = LabelFrame(settings_window, text="Temperature Unit")
        temp_frame.pack(fill=BOTH, expand=YES)
        cel_radio = Radiobutton(temp_frame, text="Celsius", variable=self.data.temp_unit, value=TEMP_C)
        cel_radio.pack()
        fah_radio = Radiobutton(temp_frame, text="Fahrenheit", variable=self.data.temp_unit, value=TEMP_F)
        fah_radio.pack()

    def change_city(self) -> None:
        """
            Listener for Change City button.
            Opens GUI for user to update their location (Updates backend data as well).
        """
        city_select_window = Toplevel(self.root)
        city_select_window.title("Enter your new location information")

        self.change_city_label = Label(city_select_window, text="Enter New Location Information Below")
        self.change_city_label.grid(row=0, column=0, columnspan=2)
        city_label = Label(city_select_window, text="City:")
        city_label.grid(row=1, column=0)
        self.new_city_entry = Entry(city_select_window)
        self.new_city_entry.grid(row=1, column=1)
        state_label = Label(city_select_window, text="State/Province:")
        state_label.grid(row=2, column=0)
        self.new_state_entry = Entry(city_select_window)
        self.new_state_entry.grid(row=2, column=1)
        country_label = Label(city_select_window, text="Country:")
        country_label.grid(row=3, column=0)
        self.new_country_entry = Entry(city_select_window)
        self.new_country_entry.grid(row=3, column=1)

        update_button = Button(city_select_window, text="Update", command=self.validate_city_change)
        update_button.grid(row=4, column=0, columnspan=2)

    def validate_city_change(self) -> None:
        """
            Listener for Update button in Change City window.
            Confirms if city is valid before updating.
        """
        res = self.data.validate_location(
            self.new_city_entry.get(),
            self.new_state_entry.get(),
            self.new_country_entry.get())
        print(res)

    def show_msg(self, msg: str, lvl: int = MSG_INFO) -> None:
        """
            Display an info/warning/error message in a new window.
        """
        if lvl == MSG_INFO:
            messagebox.showinfo(title = "Info", message = msg)
        elif lvl == MSG_WARNING:
            messagebox.showwarning(title = "Warning", message = msg)
        elif lvl == MSG_ERROR:
            messagebox.showerror(title = "Error", message = msg)
        else:
            raise ValueError("Invalid message type!")

class ClientData:
    """
        Holds all active weather data and client settings.
        Provides functions for retrieving updated weather data.
    """
    def __init__(self) -> None:
        """
            Initialize a new instance for storing client data.
        """
        self.city = "<No City Set>"
        self.state = "<No State Set>"
        self.country = "<No Country Set>"
        self.longitude = "<No Longitude Set>"
        self.latitude = "<No Latitude Set>"

        self.daily_max_temp = 0
        self.daily_min_temp = 0
        self.daily_curr_temp = 0
        self.daily_feels_like = 0

        self.curr_wind_speed = 0
        self.curr_wind_dir = 0

        self.sunrise_time = 0
        self.sunset_time = 0

        self.temp_unit = TEMP_C

        self.make_request()

    def validate_location(self, city, state, country) -> int:
        """
            Checks if a provided location tuple is a valid location with OpenWeather.
            Returns OK on success, or ERROR on failure.
        """
        print("Validating: ", city, "-", state, "-", country)
        return OK

    def make_request(self) -> int:
        """
            Make a request to the OpenWeather service.
            Returns int code reflecting request result (200, 404, etc)
        """
        url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}".format(API_KEY = MY_KEY)

        res = requests.get(url)

        # TODO: Error check result before converting to JSON!

        print(res)

        data = res.json()

        print(data)

def main() -> None:
    """
        Entry point for the program.
        Calls all other functions.
    """
    gui = Interface()
    gui.launch_interface()

if __name__ == "__main__":
    main()