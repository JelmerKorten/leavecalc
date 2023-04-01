import customtkinter
from datetime import date, timedelta

# Set appereance
customtkinter.set_appearance_mode("System") # System, Dark, Light
customtkinter.set_default_color_theme("blue") # blue / green / dark-blue

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Setup window
        self.title("Leave Calculator")
        WIDTH = 440
        HEIGHT = 300
        SWIDTH = self.winfo_screenwidth()
        SHEIGHT = self.winfo_screenheight()
        self.geometry(f"{WIDTH}x{HEIGHT}+{int((SWIDTH/2)-(WIDTH/2))}+{int((SHEIGHT/2)-(HEIGHT/2))}")

        # Create 2 entry boxes
        self.entry1 = customtkinter.CTkEntry(self, placeholder_text= "First leave date (yyyy-mm-dd)",width=200)
        self.entry1.grid(row=0, column=1, columnspan=2, padx=(10,10), pady=(20,10), sticky="nsew")
        # self.entry1.focus_set() # Not in use because it doesn't show the placeholder_text

        self.entry2 = customtkinter.CTkEntry(self, placeholder_text= "Last date or total days",width=200)
        self.entry2.grid(row=0, column=3, columnspan=2, padx=(10,10), pady=(20,10), sticky="nsew")

        # Create calculate button
        self.calc_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"), text="Calculate", command=self.leaveplanner)
        self.calc_button.grid(row=2, column=2, columnspan=2,padx=(10,10), pady=(10,10), sticky="nsew")

        # Create textbox for output
        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=3,column=1,rowspan=1,columnspan=4, padx=(10,10), pady=(10,10), sticky="nsew")
        self.textbox.configure(state="disabled")


    # Setup function for calculate button
    def leaveplanner(self):
        """Takes the first day of leave.
        outputs the dates of rotational leave that need
        to be requested.
        Assumes half paid, half unpaid, cz of weird rules.
        Will allow for either days as second argument, or
        a date."""

        first_leave_day = self.entry1.get()
        end_param = self.entry2.get()

        # To check if end date or leave days have been entered
        if len(end_param) > 3:
            total_leave_days = date.fromisoformat(end_param) - date.fromisoformat(first_leave_day) + timedelta(days=1)
            total_leave_days = total_leave_days.days


        else:
            if end_param.isdigit():
                total_leave_days = int(end_param)

        # Get date from first entry box
        start_date = date.fromisoformat(first_leave_day)

        # Calculate paid days
        paid_leave = total_leave_days/2
        paid_leave_date = start_date + timedelta(days=paid_leave-1)
        paid_days = paid_leave_date - start_date + timedelta(days=1)

        # Calculate unpaid days
        unpaid_leave_date = start_date + timedelta(days=total_leave_days-1)
        unpaid_days = unpaid_leave_date - paid_leave_date +timedelta(days=0)

        # Instead of return we have to set the text to the textbox
        self.textbox.configure(state="normal") # Activate box
        self.textbox.delete("0.0","end") # Clear old content
        self.textbox.insert("0.0", f"Take paid leave from {start_date} until {paid_leave_date} ({paid_days.days} days)\n\nTake unpaid leave from {paid_leave_date + timedelta(days=1)} until {unpaid_leave_date} ({unpaid_days.days} days)")
        self.textbox.configure(state="disabled") # Deactivate box

if __name__ == "__main__":
    app = App()
    app.mainloop()