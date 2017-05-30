# Name:  Cyrus Eftos
# Student Number: 10434000

# “quotemaster.py”, a GUI program that uses the data in the text file to quiz the user about
# the authors of the quotes.

import json
import random
import tkinter
import tkinter.messagebox


class ProgramGUI:
    def __init__(self):

        # declare empty variables
        self.authors = set()  # Stores Authors set
        self.buttons = []  # Store tkinter buttons in list for looping over later in the program
        self.count = 0  # Store asked question count
        self.data = []  # Stores loaded JSON
        self.random_quote = {}  # Stores a random quote that is grabbed in the load_quote() function
        self.remaining = 0  # Stores time remaining
        self.score = 0  # Stores current score
        self.timer_id = None  # Stores the timer
        self.year_said = ''

        try:
            with open('data.txt', 'r') as outfile:
                self.data = json.load(outfile)
        except FileNotFoundError:  # catch FileNotFoundError exception
            tkinter.messagebox.showerror('Error', 'Missing or Invalid file')
            self.quit()
        except ValueError:  # catch ValueError exception
            tkinter.messagebox.showerror('Error', 'Empty file or Invalid JSON syntax')
            self.quit()

        # Sort author information and use .update() to remove duplicates
        for x in self.data:
            self.authors.update([x['author']])

        if len(self.authors) < 3:
            tkinter.messagebox.showerror('Error', 'Insufficient number of authors')
            self.quit()
    


        # Instantiate tkinter and set parameters
        self.main = tkinter.Tk()
        self.main.geometry('550x330')
        self.main.resizable(False, False)
        self.main.title('QuoteMaster')

            
        # Instantiate frames
        progress_frame = tkinter.Frame(self.main)
        heading_frame = tkinter.Frame(self.main)
        quote_frame = tkinter.Frame(self.main)
        bottom_frame = tkinter.Frame(self.main)

        # Pack frames
        progress_frame.pack(fill="x", padx=20, pady=10)
        heading_frame.pack(fill="x")
        quote_frame.pack(expand=1, fill="both")
        bottom_frame.pack(fill="x")
        

        # Instantiate tkinter.Frame() and assign to bottom_buttons_frame then pack.
        bottom_buttons_frame = tkinter.Frame(bottom_frame)
        bottom_buttons_frame.pack(expand=1, pady=(10, 20))

        # Instantiate tkinter.Label() and assign to progress_score_label then pack.
        self.progress_score_label = tkinter.Label(progress_frame, anchor='w', font=('Tahoma bold', 13))
        self.progress_score_label.pack(side="left", expand="yes", fill="x")    

        # Instantiate tkinter.Label() and assign to heading_label then pack.
        self.heading_label = tkinter.Label(heading_frame, text="Who said...", font=('Tahoma bold', 13))
        self.heading_label.pack(side="left", expand="yes", fill="x")

        # Instantiate tkinter.Label() and assign to progress_timer_label then pack.
        self.progress_timer_label = tkinter.Label(progress_frame, anchor='e', fg='#4990E2', font=('Tahoma bold', 13))
        self.progress_timer_label.pack(side="left", expand="yes", fill="x")

        # Instantiate tkinter.Label() and assign to quote_label then pack.
        self.quote_label = tkinter.Label(quote_frame)
        self.quote_label.configure(wraplength=460, font=('Tahoma bold', 22), justify='center')
        self.quote_label.pack(expand=1)

        # Loop over a range of 3 to push Button(s) into the self.buttons list.
        # This seemed like a more logical way of creating the buttons since they don't need to
        # have any attributes attached until the load_quote function is used.
        for i in range(3):
            button = tkinter.Button(bottom_buttons_frame, padx=20, pady=5)
            button.grid(column=i, row=0, padx=10)
            self.buttons.append(button)

        self.load_quote()  # load quote function
        self.main.mainloop()  # mainloop stuff

    def start_countdown(self, remaining=None):
        self.progress_timer_label.configure(fg='#4990E2')  # Make label text blue
        if remaining is not None:
            self.remaining = remaining
        if self.remaining <= 4:  # This should be a "3" but for some reason it changes the colour @ 0:02 so started at '4"
            self.progress_timer_label.configure(fg='#D0011B')  # Make label text red
        self.remaining -= 1  # decrease self.remaining by 1

        # Assign self.main.after(x,x) to self.timer_id. This is used to cancel the timer when an answer is checked
        # otherwise the timer will speed up.
        self.timer_id = self.main.after(1000, self.start_countdown)
        # update the progress_timer_label with the current time remaining. zfill() pads the number to 2 digits.
        self.progress_timer_label.configure(text='Time Remaining: 00:' + str(self.remaining).zfill(2))
        # when the counter reaches 0. stop the timer and load a new quote.
        if self.remaining < 1:
            self.main.after_cancel(self.timer_id)
            self.load_quote()

    def answer_percentage(self):
        return str(int(100 * float(self.score) / float(self.count))) + '%'

    def quit(self):
        return self.main.destroy()

    def load_quote(self):
        self.start_countdown(11)
        self.count += 1  # increment self.questionCount
        # grab a random quote from the self.data list
        self.random_quote = random.choice(self.data)
        # set self.quoteLabel text with the random quote that is loaded.
        self.quote_label.configure(text='"{}"'.format(self.random_quote['quote']))
        self.progress_score_label.configure(text='Score: ' + str(self.score) + ' / ' + str(self.count - 1))
        # Take the "self.authors" set and remove the author of the random quote (difference), then take a random
        # sample of two authors and finally add the the removed random quote author back into the set (union).
        random_authors = set(random.sample(self.authors - {self.random_quote['author']}, 2)) | set([self.random_quote['author']])
        # Iterate over the re-randomised random_authors (can't seem to get random.shuffle() too work on a set) and set
        # the button titles and functions. author=author makes sure the current variable from the loop is passed to the
        # checkAnswer() author parameter.
        for key, author in enumerate(random.sample(random_authors, 3)):
            self.buttons[key].configure(text=author, command=lambda author=author: self.check_answer(author))

    def check_answer(self, chosen_name):
        self.main.after_cancel(self.timer_id)
        year_said = ''  # declare empty year_said variable
        if chosen_name == self.random_quote['author']:  # Check answer
            current_result = "Correct!"
            self.score += 1
            # if "random_quote['year']" is not "u" return "It was said in xxxx" or return an empty string.
            year_said = '\nIt was said in ' + str(self.random_quote['year']) if self.random_quote['year'] != 'u' else ''
        else:
            current_result = "Incorrect!"
        bloop = str(self.score) + ' / ' + str(self.count) + ' (' + str(self.answer_percentage()) + ')'
        message = 'You\'re ' + str(current_result) + str(year_said) + '\nYour score is ' + str(
            bloop) + '\n\nContinue?'
        if tkinter.messagebox.askyesno(current_result, message):
            self.load_quote()
        else:
            self.quit()


# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()
