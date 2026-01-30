import tkinter as tk

class ft_gui:
    def __init__(self, headtracker):
        self.headtracker = headtracker

        self.read_only_root = {"relative x":"rel_x", "relative y":"rel_y", "percentage x":"percentage_x", "percentage y":"percentage_y"}
        self.read_only_value_labels = []
        self.maluable_root = {"x scale":"x_scale","y scale":"y_scale","deadzone base":"deadzone_base","eye threshold":"threshold"}
        self.maluable_value_labels = []

        self.window_bgColour = "#a7a7a7"
        self.frame_titlebgColour = "#444343"
        self.frame_widget_bgColour = "#e8e8e8"
        self.frame_borderColour = "#000000"
        
        self.frame_width = 412
        self.label_width = self.frame_width/2

        self.window = tk.Tk()
        self.window.title("Face Tracker")
        self.window.geometry("467x600")
        
        self.logo = tk.PhotoImage(file="assets/logo.png")
        self.window.iconphoto(True, self.logo)  
        self.window.config(background=self.window_bgColour)

        self.window.protocol("WM_DELETE_WINDOW", self.kill_ht)

        self.monitor_frame = tk.Frame(self.window, width = self.frame_width, height=1, bd=2, relief="solid", highlightcolor=self.frame_borderColour)
        self.monitor_frame.pack(pady=20)
        self.monitor_frame.pack_propagate(False)
        self.monitor_frame.grid_propagate(True)
        
        self.system_settings = tk.Frame(self.window, width = self.frame_width, bd=2, relief="solid", highlightcolor=self.frame_borderColour)
        self.system_settings.pack(pady=20)
        self.system_settings.pack_propagate(False)
        self.system_settings.grid_propagate(True)

        self.mf_title = tk.Label(self.monitor_frame, text="System Monitor", bg=self.frame_titlebgColour)
        self.mf_title.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.ss_title = tk.Label(self.system_settings, text="System Settings", bg=self.frame_titlebgColour)
        self.ss_title.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        for i, (k, _) in enumerate(self.read_only_root.items()):
            temp_name = tk.Label(self.monitor_frame, text=k, bg=self.frame_widget_bgColour)
            temp_value = tk.Label(self.monitor_frame, text="-1", bg=self.frame_widget_bgColour)
            temp_name.grid(row=i+1, column=0, columnspan=1, sticky="ew")
            temp_value.grid(row=i+1, column=1, columnspan=1, sticky="ew")
            self.read_only_value_labels.append(temp_value)
        for i, (k, v) in enumerate(self.maluable_root.items()):
            temp_name = tk.Label(self.system_settings, text=k, bg=self.frame_widget_bgColour)
            temp_value = tk.Entry(self.system_settings, bg=self.frame_widget_bgColour)
            temp_value.insert(0, getattr(self.headtracker, v))
            temp_name.grid(row=i+1, column=0, columnspan=1, sticky="ew")
            temp_value.grid(row=i+1, column=1, columnspan=1, sticky="ew")
            self.maluable_value_labels.append(temp_value)
            
        self.monitor_frame.grid_columnconfigure(0, weight=1, minsize=self.label_width)
        self.monitor_frame.grid_columnconfigure(1, weight=1, minsize=self.label_width)
        self.system_settings.grid_columnconfigure(0, weight=1, minsize=self.label_width)
        self.system_settings.grid_columnconfigure(1, weight=1, minsize=self.label_width)

        self.submit_button = tk.Button(self.window, text ="Submit", command=self.submit)
        self.submit_button.pack()
    def submit(self):
        for i, (_, v) in enumerate(self.maluable_root.items()):
            input = self.maluable_value_labels[i].get()
            try:
                value = float(input)
                setattr(self.headtracker, v, value)
                print("Submited", v, value, "////", getattr(self.headtracker, v))
            except ValueError:
                print("Value Error")
    def update(self):
        for i, (_, v) in enumerate(self.read_only_root.items()):
            if getattr(self.headtracker, v) is not None:
                value = round(getattr(self.headtracker, v), 1)
                self.read_only_value_labels[i].config(text=value)
        self.window.after(50, self.update)
    def run(self):
        self.update()
        self.window.mainloop()
    def kill_ht(self):
        self.headtracker.stop()
        self.window.destroy()