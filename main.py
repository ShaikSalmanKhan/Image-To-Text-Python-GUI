from tkinter import *
from tkinter import filedialog
import pyperclip
from PIL import Image, ImageTk
from datetime import datetime
import pytesseract
import pywhatkit


IMAGE_FORMATS    = [("PNG", "*.png")]
BACKGROUND_COLOR = "#2c061f"
NUMBER_TO_SEND   = ""  # replace with whatsapp number (to send message)
# pytesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"


def send_message():
    """This function will send extracted text to whatsapp"""
    # disabling the whatsapp button , whatsapp label
    whatsapp_label.config(text="✔ Sent", bg=BACKGROUND_COLOR, fg="white")
    whatsapp_button.config(state=DISABLED)

    # getting current hour & minute from datetime module
    hour = datetime.now().time().hour
    min  = datetime.now().time().minute
    pywhatkit.sendwhatmsg(NUMBER_TO_SEND, extracted_text, hour, min+1)


def show_whatsapp_buttons():
    """it is used to enable whatsapp button , whatsapp_label on the screen"""
    global whatsapp_button, whatsapp_label
    whatsapp_button.grid(row=4, column=0, pady=5)
    whatsapp_label.grid(row=5, column=0, pady=5)


def convert_to_text():
    global extracted_text

    # once convert button is clicked --> disable it & change its text
    convert_button.config(text="✔ Converted & Copied Text to Clipboard", bg=BACKGROUND_COLOR, fg="white")
    convert_button.config(state=DISABLED)

    # using pytesseract extracting the text from the image
    img              = Image.open(path)
    extracted_text   =  pytesseract.image_to_string(img)
    extracted_text   =  extracted_text.replace('\n', " ")
    extracted_text   =  extracted_text.replace(extracted_text[-1], '')
    # print(extracted_text)
    finding_dot      = extracted_text.find(".")
    first_line       = extracted_text[:finding_dot]
    next_line        = extracted_text[finding_dot+1:]

    # copying the text to clipboard
    pyperclip.copy(extracted_text)

    # showing the text in the app
    converted_text_label = Label()
    converted_text_label.config(text=f"{first_line} \n {next_line}")
    converted_text_label.config(bg=BACKGROUND_COLOR, font=("Times", 12, "bold"), fg="white")
    converted_text_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

    # showing whatsapp buttons
    show_whatsapp_buttons()


def show_image(filepath):
    """it will show the selected image in the screen"""
    global path
    path            = filepath

    # placing the selected image in the screen
    load_image      = Image.open(path)
    render_image    = ImageTk.PhotoImage(load_image)
    image_label     = Label(image=render_image)
    image_label.img = render_image
    width           = render_image.width()
    height          = render_image.height()
    image_label.config(width=width, height=height)
    image_label.grid(row=1, column=0, columnspan=2, padx=20)

    # placing the convert button after image is placed in the screen
    convert_button.grid(row=2, column=0, columnspan=2, padx=20, pady=5)


def upload_image():
    """it is used to upload image in the screen"""
    # upload image ----> 137 x 139
    file_path = filedialog.askopenfilename(filetypes=IMAGE_FORMATS, title='Please select a image')
    show_image(file_path)


# --------------------------UI----------------------------------
# creating a window,setting its size, title, bg color
window = Tk()
window.title("Image To Text")
window.geometry("340x440")
window.resizable(0, 0)
window.config(bg=BACKGROUND_COLOR)

app_title = Label()
app_title.config(text="Image To Text", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, fg="white")
app_title.grid(row=0, column=0, pady=20, padx=70)

# -----------------------Upload Image Label----------------------------------
upload_button = Button(text='Upload Image', command=upload_image)
upload_button.grid(row=1, column=0, columnspan=2, padx=20)

# ------------------------Convert Button------------------------
convert_button = Button(text='Convert', command=convert_to_text)

# Creating a button named as whatsapp with its photo
photo           = PhotoImage(file="whatsapp.PNG")
whatsapp_button = Button()
whatsapp_button.config(image=photo, command=send_message, width=75, height=75, highlightthickness=0)

# label for whatsapp
whatsapp_label = Label()
whatsapp_label.config(text="Send to Whatsapp (click on the image)", bg=BACKGROUND_COLOR, fg="white")


window.mainloop()
