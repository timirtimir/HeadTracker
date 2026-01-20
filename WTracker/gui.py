import tkinter as tk

class ft_gui:
    def __init__(self, headtracker):
        self.headtracker = headtracker

        self.read_only_root = {"relative x":"rel_x", "relative y":"rel_y", "percentage x":"percentage_x", "percentage y":"percentage_y"}
        self.read_only_value_labels = []
        self.maluable = []

        self.window_bgColour = "#a7a7a7"
        self.frame_titlebgColour = "#444343"
        self.frame_widget_bgColour = "#e8e8e8"
        self.frame_borderColour = "#000000"

        self.window = tk.Tk()
        self.window.title("Face Tracker")
        self.window.geometry("467x600")
        
        self.logo = tk.PhotoImage(file="assets/logo.png")
        self.window.iconphoto(True, self.logo)  
        self.window.config(background=self.window_bgColour)

        self.monitor_frame = tk.Frame(self.window, width = 412, height = 145, bd=2, relief="solid", highlightcolor=self.frame_borderColour)
        self.monitor_frame.pack(pady=20)
        self.monitor_frame.pack_propagate(False)

        self.mf_title = tk.Label(self.monitor_frame, text="System Monitor", bg=self.frame_titlebgColour)
        self.mf_title.grid(row=0)
        
        for i, (k, _) in enumerate(self.read_only_root.items()):
            temp_name = tk.Label(self.monitor_frame, text=k, bg=self.frame_widget_bgColour)
            temp_value = tk.Label(self.monitor_frame, text="-1", bg=self.frame_widget_bgColour)
            temp_name.grid(row=i+1, column=0)
            temp_value.grid(row=i+1, column=1)
            self.read_only_value_labels.append(temp_value)
    def update(self):
        for i, (_, v) in enumerate(self.read_only_root.items()):
            value = round(getattr(self.headtracker, v), 1)
            self.read_only_value_labels[i].config(text=value)
        self.window.after(50, self.update)
    def run(self):
        self.update()
        self.window.mainloop()