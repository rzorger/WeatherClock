import tkinter as tk
import time

def update_clock(label):
    label.config(text=time.strftime('%H:%M'))
    label.after(1000, update_clock, label)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Fullscreen mode
    root.configure(bg='black')
    root.bind('<Escape>', lambda e: root.destroy())  # Exit on Esc key
    
    clock_label = tk.Label(root, font=('Helvetica', 100), fg='white', bg='black')
    clock_label.pack(side='top', pady=20)  # Position at top center with padding

    update_clock(clock_label)
    root.mainloop()

if __name__ == "__main__":
    main()

