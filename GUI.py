import tkinter as tk
from tkinter import font, Toplevel, Label, Entry, Button, Listbox, Scrollbar
from ExcelScreenshotTaker import ExcelScreenshotTaker
from WordpressAutomation import WordpressAutomation as wp
import GenerateGPTArticle
import os

window = tk.Tk()
window.title("## Project 2500 ##")

window.geometry("1024x512") 
window.configure(bg="black")  

button_bg_color = "#2e5da1"  
button_fg_color = "white"  

def open_first_dialog():
    first_dialog = Toplevel(window)
    first_dialog.title("Enter Details")
    first_dialog.configure(bg="black")
    first_dialog.geometry("900x700")

    user_inputs = {
        "USERNAME": "ahmedhelmey006@gmail.com",
        "PASSWORD": '090197Aa'
    }

    top_div = tk.Frame(first_dialog)
    top_div.pack(fill=tk.BOTH, expand=False)

    middle_div = tk.Frame(first_dialog)
    middle_div.pack(fill=tk.BOTH, expand=True)

    bottom_div = tk.Frame(first_dialog)
    bottom_div.pack(fill=tk.BOTH, expand=False)

    excel_prompt = Label(top_div, text="Enter the Excel Folder Location:")
    excel_prompt.pack(padx=10, pady=5, anchor="w")

    excel_input = Entry(top_div)
    excel_input.pack(padx=10, pady=5, fill="x", anchor="w")

    def get_excel_location():
        user_inputs['excel_path'] = excel_input.get()

    excel_confirm_button = Button(top_div, text="Confirm", bg="black", fg=button_fg_color, command=get_excel_location)
    excel_confirm_button.pack(padx=10, pady=5, anchor="e")

    image_prompt = Label(top_div, text="Enter the Image Folder Location:")
    image_prompt.pack(padx=10, pady=5, anchor="w")

    image_input = Entry(top_div)
    image_input.pack(padx=10, pady=5, fill="x", anchor="w")

    def get_images_location():
        user_inputs['image_path'] = image_input.get()

    image_confirm_button = Button(top_div, text="Confirm", bg="black", fg=button_fg_color, command=get_images_location)
    image_confirm_button.pack(padx=10, pady=5, anchor="e")

    prompt_prompt = Label(bottom_div, text="Enter a prompt:")
    prompt_prompt.pack(padx=10, pady=5, anchor="w")

    prompt_input = Entry(bottom_div)
    prompt_input.pack(padx=10, pady=5, fill="x", anchor="w")

    def assign_prompt():
        global prompt
        prompt = prompt_input.get()

    confirm_button = Button(bottom_div, text="Confirm", command=assign_prompt, bg="black", fg=button_fg_color)
    confirm_button.pack(padx=10, pady=5, anchor="e")

    left_half = tk.Frame(middle_div)
    left_half.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_half = tk.Frame(middle_div)
    right_half.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    listbox_add_entry = Entry(left_half)
    listbox_add_entry.pack(padx=10, pady=30, fill="x")

    def add_item():
        item = listbox_add_entry.get()
        if item:
            options.append(item)  # Add the item to the options list
            listbox.insert(tk.END, item)
            listbox_add_entry.delete(0, tk.END)


    add_button = Button(left_half, text="Add", command=add_item, width=15, height=1, bg="black", fg=button_fg_color)
    add_button.pack(pady=30)

    def remove_item():
        selected_indices = listbox.curselection()
        for i in selected_indices:
            listbox.delete(i)

    remove_button = Button(left_half, text="Remove", command=remove_item, width=15, height=1, bg="black", fg=button_fg_color)
    remove_button.pack(pady=30)

    tags_label = Label(right_half, text="Select Tags:")
    tags_label.pack(padx=10, pady=5, anchor="w")

    options = ["Project Management", "Free Excel Template"]
    
    listbox = Listbox(right_half, selectmode=tk.MULTIPLE)
    listbox.pack(fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(right_half, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)

    for option in options:
        listbox.insert(tk.END, option)

    def choose_options():
        selected_indices = listbox.curselection()

        # Ensure you're not accessing out-of-range indices
        if max(selected_indices, default=-1) < len(options):
            user_inputs['selected_options'] = [options[i] for i in selected_indices]
            selected_options_label.config(text=", ".join(user_inputs['selected_options']))
        else:
            print("Unexpected selection index detected.")

    choose_button = Button(right_half, text="Choose", command=choose_options, width=15, height=1, bg="black", fg=button_fg_color)
    choose_button.pack()

    def execute():
        wp_automation = wp()
        wp_automation.create_post(user_inputs["USERNAME"], user_inputs["PASSWORD"], user_inputs["excel_path"], user_inputs["image_path"], user_inputs["selected_options"])

    execute_button = Button(bottom_div, text="Execute", width=15, height=1, font=button_style, bg="black", fg="white", command=execute)
    execute_button.pack(pady=10, padx=10)

    selected_options_label = Label(right_half, text="", fg="black")
    selected_options_label.pack()


def open_second_dialog():
    second_dialog = Toplevel(window)
    second_dialog.title("Generate Article")
    second_dialog.configure(bg="black")  # Set the background color of the dialog to black
    second_dialog.geometry("900x700")  # Set the size of the dialog

    # Create divs using frames
    first_div = tk.Frame(second_dialog)
    first_div.pack(fill=tk.BOTH, expand=True)  # Set expand to True

    second_div = tk.Frame(second_dialog)
    second_div.pack(fill=tk.BOTH, expand=True)  # Set expand to True

    # Split the first_div into two halves horizontally
    left_half = tk.Frame(first_div)
    left_half.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_half = tk.Frame(first_div)
    right_half.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    article_input = Entry(right_half, font=button_style)
    article_input.pack(padx=10, pady=5, fill="both", expand=True)

    # Add an output container in the right half
    output_label = Label(right_half, text="Generated Article:", font=button_style)
    output_label.pack(padx=10, pady=5, anchor="w")

    output_text = tk.Text(right_half, font=button_style, wrap=tk.WORD)
    output_text.pack(padx=10, pady=5, fill="both", expand=True)

    # Add "Copy Article" and "Generate Article" buttons in the second_div
    copy_article_button = Button(second_div, text="Copy Article", bg="black", fg=button_fg_color)
    copy_article_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    generate_article_button = Button(second_div, text="Generate Article", bg="black", fg=button_fg_color)
    generate_article_button.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)



def open_third_dialog():
    third_dialog = Toplevel(window)
    third_dialog.title("Enter Details")
    third_dialog.geometry("500x300") 
    user_input = {}

    # Create divs using frames
    top_div = tk.Frame(third_dialog)
    top_div.pack(fill=tk.BOTH, expand=False)  # Set expand to False

    def get_excel_location():
        user_input['excel_path'] = excel_input.get()

    excel_prompt = Label(top_div, text="Enter the Excel Folder Location:")
    excel_prompt.pack(padx=10, pady=5, anchor="w")


    excel_input = Entry(top_div)
    excel_input.pack(padx=10, pady=5, fill="x", anchor="w")

    excel_confirm_button = Button(top_div, text="Confirm", bg="black", fg=button_fg_color, command=get_excel_location)
    excel_confirm_button.pack(padx=10, pady=5, anchor="e")

    # Prompt 2: Enter the Image Folder Location in top div
    image_prompt = Label(top_div, text="Enter the Image Folder Location:")
    image_prompt.pack(padx=10, pady=5, anchor="w")

    def get_imge_save_location():
        user_input['img_path'] = excel_input.get()

    image_input = Entry(top_div)
    image_input.pack(padx=10, pady=5, fill="x", anchor="w")

    image_confirm_button = Button(top_div, text="Confirm", bg="black", fg=button_fg_color, command= get_imge_save_location)
    image_confirm_button.pack(padx=10, pady=5, anchor="e")

    def take_screenshots(folder_path, save_folder):

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            save_path = os.path.join(save_folder, os.path.splitext(file_name)[0] + ".png")

            screenshot_taker = ExcelScreenshotTaker(file_path, save_path)
            screenshot_taker.run()


    execute_button = Button(top_div, text="Execute", width=15, height=1, font=button_style, bg="black", fg="white", command=lambda: take_screenshots(user_input["excel_path"], user_input["excel_path"]))
    execute_button.pack(pady=10, padx=10)


main_line_font = font.Font(family="Helvetica", size=24, weight="bold")

label_text = "Hello said, What do you want to do today?"
label = Label(window, text=label_text, font=main_line_font, padx=20, pady=20, fg="white", bg="black")
label.pack()

button_style = font.Font(family="Helvetica", size=12, weight="bold")
ScreenShotTaker = Button(window, text="Take Screenshots", command=lambda:open_third_dialog(),  width=15, height=1, font=button_style, bg=button_bg_color, fg=button_fg_color)
ArticleGenerator = Button(window, text="Generate Article", command=lambda: open_second_dialog(), width=15, height=1, font=button_style, bg=button_bg_color, fg=button_fg_color)
WPAutomation = Button(window, text="Create Posts", command=lambda: open_first_dialog(), width=15, height=1, font=button_style, bg=button_bg_color, fg=button_fg_color)

ScreenShotTaker.pack(side=tk.BOTTOM, padx=10, pady=10)
ArticleGenerator.pack(side=tk.BOTTOM, padx=10, pady=10)
WPAutomation.pack(side=tk.BOTTOM, padx=10, pady=10)

window.mainloop()
