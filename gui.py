from tkinter import *
from backend import *

#TODO: import the data interface
#TODO: import the model interface

#==============================
#| CONFIGS
#==============================
BG_GRAY = "burlywood3"
BG_COLOR = "burlywood2"
TEXT_COLOR = "black"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

bot_name = "BOT_NAME"

class ChatBot:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.previous_team = ""
        self.botname = bot_name
        self.mm = ModelManager()

        
    def run(self):
        self.window.mainloop()
        
        
    def _setup_main_window(self):
        self.window.title("ChatBot")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg="black",
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        #repurposed as a drop down menu
        #for some reason the relpos feature of tkinter is very hard to work with, so the tiny bar under "welcome" is the drop down, need to figure out how to change that.
        #line = Label(self.window, width=450, bg="darkgoldenrod3")
        options = get_teams()
        selected = StringVar(self.window)
        selected.set(options[0])
        drop_down = OptionMenu(self.window, selected, *options)
        drop_down.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry = Entry(bottom_label, bg="burlywood4", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None, selected))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        
    def _on_enter_pressed(self, event, selected):
        if((self.previous_team == "")|(self.previous_team != selected.get())):
            create_retriever(selected.get())
            self.previous_team = selected.get()
            
            #self.msg_entry.delete(0, END)
            msg = f"{bot_name}: Hi there, you've now switched over to {self.previous_team} team.\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg)
            self.text_widget.configure(state=DISABLED)
            self.text_widget.see(END)
            
        msg = self.msg_entry.get()
        print("Naaz", msg)

        self._insert_message(msg, "You")
            
    def _insert_message(self, msg, sender):
        if not msg:
            return
            
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        msg2 = f"{bot_name}: {get_response(self.mm, msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)


#boiler plate code guard
#creates ChatBot instance and run
if __name__ == "__main__":
    app = ChatBot()
    
    app.run()
