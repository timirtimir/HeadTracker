from HeadTracker import HeadTracker
from gui import ft_gui
import threading

def main():
    HT = HeadTracker()
    ht_gui = ft_gui(HT)

    thread = threading.Thread(target=HT.run)
    thread.start()
    
    ht_gui.run()
    
if __name__ == "__main__":
    main()