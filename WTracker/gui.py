import tkinter as tk

class ft_gui:
    def __init__(self):
        self.frame_bgColour = "#a7a7a7"
        self.frame_titlebgColour = "#444343"
        self.frame_widget_bgColour = "#e8e8e8"
        self.frame_borderColour = "#000000"

        self.window = tk.Tk()
        self.window.title("Face Tracker")
        self.window.geometry("467x600")
        
        self.logo = tk.PhotoImage(file="assets/logo.png")
        self.window.iconphoto(True, self.logo)  
        self.window.config(background="#cbced4")

        self.monitor_frame = tk.Frame(self.window, width = 412, height = 145, bd=2, relief="solid", highlightcolor=self.frame_borderColour, bg=self.frame_bgColour)
        self.monitor_frame.pack(pady=20)
        self.monitor_frame.pack_propagate(False)
        self.mf_title = tk.Label(self.monitor_frame, text="System Monitor", bg=self.frame_titlebgColour)
        
        self.settings_frame = tk.Frame(bg=self.frame_bgColour)

        self.window.mainloop()
ft_gui()