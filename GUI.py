from tkinter import *
from PIL import Image, ImageTk
import speechto
import action  # Make sure this module exists with an Action function

root = Tk()
root.title("AI Assistant")
root.geometry("550x675")
root.resizable(FALSE, False)
root.config(bg="#6F8FAF")

# ask function
def ask():
    user_val = speechto.speech_to_text()
    bot_val = action.Action(user_val)
    text.insert(END, 'user--->' + user_val + "\n")
    if bot_val is not None:
        text.insert(END, "BOT<---" + str(bot_val) + "\n")
    if bot_val == "ok sir":
        root.destroy()

def send():
    send_text = entry.get()
    bot = action.Action(send_text)
    text.insert(END, 'user--->' + send_text + "\n")
    if bot is not None:
        text.insert(END, "BOT<---" + str(bot) + "\n")
    entry.delete(0, END)  # Clear the entry box after sending
    if bot == "ok sir":
        root.destroy()

def del_text():
    text.delete('1.0', "end")

# frame
frame = LabelFrame(root, padx=100, pady=7, borderwidth=3, relief="raised")
frame.config(bg="#6F8FAF")
frame.grid(row=0, column=1, padx=55, pady=10)

# text label
text_label = Label(frame, text="AI Assistant", font=("Comic Sans MS", 14, "bold"), bg="#356696")
text_label.grid(row=0, column=0, padx=20, pady=10)

# image
try:
    image = ImageTk.PhotoImage(Image.open("image/Assistant.png"))
    image_label = Label(frame, image=image)
    image_label.grid(row=1, column=0, pady=0.5)
except Exception as e:
    print(f"Error loading image: {e}")
    # Fallback if image can't be loaded
    placeholder_label = Label(frame, text="Assistant Image", height=10, width=20, bg="#356696")
    placeholder_label.grid(row=1, column=0, pady=0.5)

# Adding text
text = Text(root, font=('courier 10 bold'), bg="#356696")
text.place(x=100, y=375, width=375, height=100)

# entry widget
entry = Entry(root, justify=CENTER)
entry.place(x=100, y=500, width=350, height=30)

# buttons - now with command callbacks
button1 = Button(root, text="ASK", bg="#356696", pady=16, padx=40, 
                borderwidth=3, relief=SOLID, command=ask)
button1.place(x=70, y=575)

button2 = Button(root, text="SEND", bg="#356696", pady=16, padx=40, 
                borderwidth=3, relief=SOLID, command=send)
button2.place(x=400, y=575)

button3 = Button(root, text="DELETE", bg="#356696", pady=16, padx=40, 
                borderwidth=3, relief=SOLID, command=del_text)
button3.place(x=225, y=575)

root.mainloop()
