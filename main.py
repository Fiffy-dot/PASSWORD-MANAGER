from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letters_list = [random.choice(letters) for char in range(nr_letters)]
    symbols_list = [random.choice(symbols) for sym in range(nr_symbols)]
    numbers_list = [random.choice(numbers) for num in range(nr_numbers)]
    password_list = letters_list + symbols_list + numbers_list
    random.shuffle(password_list)

    new_password = ''.join(password_list)  # join list items into string

    password_ans.insert(0, string=new_password)  # populate password field with new one

    pyperclip.copy(new_password)  # copy password to clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    #  get user entries
    website_entry = website_ans.get()
    email_entry = email_username_ans.get()
    password_entry = password_ans.get()
    new_data = {
        website_entry: {
            "email": email_entry,
            "password": password_entry,
        }
    }

    # ensure fields are not empty
    if len(website_entry) == 0 or len(email_entry) == 0 or len(password_entry) == 0:
        messagebox.showinfo(title='Error', message="Fields cannot be empty")
    else:
        # verify details
        is_okay = messagebox.askokcancel(title=website_entry, message=f"Details Entered: \nEmail: {email_entry}\n"
                                                                      f"Password:{password_entry} \nDo you want to save?")
        if is_okay:
            messagebox.showinfo(title='Success!', message=f"{website_entry} data successfully added to database!")
            try:
                with open("data.json", "r") as data_file:
                    # read our data
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    # write data to new file
                    json.dump(new_data, data_file, indent=4)

            else:
                # update our data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # save updated data
                    json.dump(data, data_file, indent=4)

            finally:
                # clear entry fields
                website_ans.delete(0, END)
                password_ans.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_data = website_ans.get()
    # read from json file
    try:
        with open("data.json", "r") as data_file:
            # read our data
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")

    else:
        # check if the website user is looking for is in our database
        if website_data in data.keys():
            messagebox.showinfo(title=website_data, message=f"Email: {data[website_data]['email']}\n"
                                                            f"Password: {data[website_data]['password']}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_data} website exists")


# ---------------------------- UI SETUP ------------------------------- #
# window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# labels
website = Label(text="Website:")
website.grid(row=1, column=0)
email_username = Label(text="Email/Username:", pady=10)
email_username.grid(row=2, column=0)
password = Label(text="Password:", pady=10)
password.grid(row=3, column=0)

# entries
website_ans = Entry()
website_ans.focus()
website_ans.grid(row=1, column=1, )
email_username_ans = Entry(width=39)
email_username_ans.insert(0, "user@gmail.com")
email_username_ans.grid(row=2, column=1, columnspan=2)
password_ans = Entry(width=21)
password_ans.grid(row=3, column=1)

# buttons
search_button = Button(text="Search", command=find_password, width=15)
search_button.grid(row=1, column=2)
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2)
add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
