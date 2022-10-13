from cProfile import label
from cgitb import text
from tkinter import *
import tkinter as tk
import time
import threading
import random
from turtle import width
from PIL import ImageTk, Image
from PIL import Image, ImageTk

class TypeSpeedGUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("Typing Speed GUI")
        self.root.geometry("1000x600")
        self.root.minsize(1000, 600)
        self.root.maxsize(1000, 600)
        self.root.configure(bg="#202020")
        # I create and configure the root, minimal size, and maximum size so that the application remains untampered. 

        self.texts = open("text.txt", "r").read().split("\n")
        # I open the text file with all the sentences I have and then split each sentance based on a new line in the text file. 

        self.frame = tk.Frame(self.root)
        self.frame.configure(bg="#202020")
        # I create a frame variable and configure the background color to a grey black color so that the frame isn't white. 

        self.root.bind('<Return>', self.start)
        # I bend return to the function start, so the WPM may continue accuretely.

        self.sampleText = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 25, "bold"), fg="#2AE98D", bg="#202020")
        self.sampleText.grid(row=0, column=0, columnspan=2, padx=5, pady=13)
        # I create the sample text. 

        self.enterNote = tk.Label(self.frame, text="Note: Press enter after completeting entry to continue typing.", font=("Helvetica", 12), fg="white", bg="#202020")
        self.enterNote.grid(row=1, column=0, columnspan=2, padx=5, pady=0)
        # I create the the note for using enter to continue typing

        def entryClick(event):
            if self.userEntry.get() == 'Type green text here':
                self.userEntry.delete(0, "end") #This delets all text in the entry.
                self.userEntry.insert(0, '') #This inserts blank for the entry.
        def focusOut(event):
            if self.userEntry.get() == '':
                self.userEntry.insert(0, 'Type green text here')
                self.userEntry.config(fg='grey')
                # The focusout will insert text on instructing the user on where to start typing. 

        self.userEntry = tk.Entry(self.frame, fg='grey', bg="#1E2824", width=40, font=("Helvetica", 24))
        self.userEntry.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.userEntry.insert(0,'Type green text here')
        self.userEntry.bind("<KeyRelease>", self.start)
        self.userEntry.bind('<FocusIn>', entryClick)
        self.userEntry.bind('<FocusOut>', focusOut)
        # I create the userEntry entry and bind it to the key release so that it detects each letter on the key release. I also insert default text as type green text here and cofus in and out to the respective functions. 

        

        self.speedLabel = tk.Label(self.frame, text="Speed: \n0.00 CPS(Characters per second)\n0.00 CPM(Characters per minute)\n0.00 WPS(Words per second)\n0.00 WPM(Words per minute)", font=("Helvetica", 18), fg="white", bg="#202020")
        self.speedLabel.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        # This is the orignal speed label I create

        self.resetButton = tk.Button(self.frame, text="Reset", command=self.reset, font=("Helvetica", 24))
        self.resetButton.grid(row=4, column=0, columnspan=1, padx=5, pady=10)
        # I create the reset button

        self.imageButton = tk.Button(self.frame, text="Generate Image?", font=("Helvetica", 24), command=self.newImage)
        self.imageButton.grid(row=4, column=1, columnspan=1, padx=5, pady=10)
        # I create the image generator button that links to the newImage function.

        self.exit_oneButton=tk.Button(self.frame, text="Close", font=("Helvitca", 24), command=self.root.destroy)
        self.exit_oneButton.grid(row=5, column=0, columnspan=2, padx=5, pady=10)
        # I create the exit button for the root window, that destroys the entire application. 


        self.frame.pack(expand=True)
        # To prevent the window from expanding out of the frame.

        self.counter= 0 
        self.running = False
        # Initilize the counter and running detecteor. 

        self.root.mainloop()
        # Run the root mainloop

    def newImage(self):
        top = tk.Toplevel()
        top.title('Image Resizer')
        top.geometry('750x500')
        top.configure(bg="#202020")
        # I configure the title, geometry, and background for the new image window. 

        self.randomImage = ImageTk.PhotoImage(Image.open(f'Images/{str(random.randint(0,15))}.jpg').resize((500, 500)))
        # I open the image file and choose from 15 images randomly. I then resize the images to 500width by 500height.


        # \/\/\/\/\/\/CODE THAT I HAD TO SCRAP BELOW\/\/\/\/\/

        # self.widthEntry = tk.Entry(top, bg="#1E2824", fg="white", width=5, font=("Helvetica", 24))
        # self.widthEntry.grid(row=0, column=0, pady=15)

        # self.widthLabel = tk.Label(top, bg='#202020', fg="white", width=5, text='Width', font=("Helvetica", 24))
        # self.widthLabel.grid(row=1, column=0)

        # self.heightEntry = tk.Entry(top, bg="#1E2824", fg="white", width=5, text='Height here', font=("Helvetica", 24))
        # self.heightEntry.grid(row=0, column=2, pady=15)

        # self.heightLabel = tk.Label(top, bg='#202020', fg="white", width=5, text='Height', font=("Helvetica", 24))
        # self.heightLabel.grid(row=1, column=2)

        # width = self.widthEntry.get()

        # ^^^^^^^CODE THAT I HAD TO SCRAP ABOVE^^^^^^^^***IT was my original intent to make an image resizing program. 


        self.closeButton = tk.Button(top, bg="#1E2824", fg="white", width=11, text="Close Window", font=("Helvetica", 24), command=top.destroy)
        self.closeButton.grid(row=0, column=1, padx=10)
        # The close button for the image generator. 

        self.imageLabel = tk.Label(top, image=self.randomImage)
        self.imageLabel.grid(row=0, column=0)
        # This makes the image appear as a label so that it doesnt have interaction. 
            


    def start(self, event): 
        if not self.running:
            if not event.keycode in [16, 17, 18]: #To ensure that ctrl shift and 
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
                # Thist starts the timer.
        if not self.sampleText.cget("text").startswith(self.userEntry.get()):
            self.userEntry.config(fg="#F2233B")
            # This detects if the user entry is wrong and the changes the color of the text to red till the user corrects the issue(s)
        else:
            self.userEntry.config(fg="white")
            # This ensures that the text is white while the user is typing.
        if self.userEntry.get() == self.sampleText.cget('text'):
            self.running = False
            self.userEntry.config(fg="#2AE98D")
            # IF the user enters the text all right, then the text will change to the color green. 
            if event.keycode in [13]:
                self.sampleText.config(text=random.choice(self.texts))
                self.userEntry.delete(0, tk.END)
                self.running = False
                self.counter = 0
            # This event.keycode binds the enter key to reseting the text, deletiing the input, re-running and restarting the counter so your WPM doesn't lose pace. It acts as a half reset.
                



    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.userEntry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.userEntry.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speedLabel.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n{wpm:.2f} WPM")
            # This ensures that while the running detector is true the characters per second are divided by the counter. THe Words per second(WPS) are distinguised by a space and then devided my the counter. THe characters per second and words per second are multiplied by 60 to get the words per minute and characters per minute. It then prints out the speed label with 2 decemial place over. I use the f string formatting.

    def reset(self):
        self.running = False
        self.counter = 0
        self.speedLabel.config(text="Speed: \n0.00 CPS(Characters per second)\n0.00 CPM(Characters per minute)\n0.00 WPS(Words per second)\n0.00 WPM(Words per minute)")
        self.sampleText.config(text=random.choice(self.texts))
        self.userEntry.delete(0, tk.END)
        # This sets everything to the orignial values. It turns of the running detectors, sets counter to 0, sets the default speed label, picks new sample text and displays it, and deletes all the user Entry. 

TypeSpeedGUI()

# This runs the class. 
