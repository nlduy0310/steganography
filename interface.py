from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from core import *

# constants
bg_color = '#E0E0E0'
text_style = 'Segoe UI'
text_size = 12
text_color = '#3030303'
padX = 10
padY = 8

revealed_message = ''

def application():
    # window
    win = Tk()
    win.title('Steganography: Hide Message Application')
    win.geometry('700x400') 
    win['bg'] = bg_color

    # Tab control
    tabControl = ttk.Notebook(win)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Hide Message')
    tabControl.add(tab2, text='Reveal Message')
    tabControl.pack(expand=1, fill="both")

    # File path process
    file_path_text = Label(tab1, font=(text_style, text_size),text='File path:', bg=bg_color)
    file_path_text.place(x=30, y=30)

    entry_path = Entry(tab1, width=45, font=(text_style, text_size))
    entry_path.place(x=110, y=30)

    def browsefunc_input():
        cur_dir = os.getcwd()
        input_path = filedialog.askopenfilename(
            initialdir=cur_dir, title='Select file')
        entry_path.insert(END, input_path)  # add this

    button = Button(tab1, text='Browse', width=5,
                    height=1, bg=bg_color, borderwidth=2, command=browsefunc_input)
    button.place(x=580, y=28)

    # Message process
    message_text = Label(tab1, font=(text_style, text_size), text='Message:', bg=bg_color)
    message_text.place(x=30, y=80)

    entry_message = Text(tab1, width=56, height=8)
    entry_message.place(x=110, y=80)

    # Output process
    output_text = Label(tab1, font=(text_style, text_size), text='Output:', bg=bg_color)
    output_text.place(x=30, y=250)

    output_entry = Entry(tab1, width=45, font=(text_style, text_size))
    output_entry.place(x=110, y=250)

    def browsefunc_output():
        cur_dir = os.getcwd()
        output_path = filedialog.askdirectory(
            initialdir=cur_dir, title='Select directory')
        output_entry.insert(END, output_path)  # add this

    button2 = Button(tab1, text='Browse', width=5,
                    height=1, bg=bg_color, borderwidth=2, command=browsefunc_output)
    button2.place(x=580, y=248)

    # Encode process
    option = StringVar(tab1)
    option.set("Image") # default value

    w = OptionMenu(tab1, option, "Image", "Audio")
    w.pack(expand=True)
    w.place(x=400, y=290)

    def handle_encode():
        print('Encode')
        print(entry_path.get())
        print(entry_message.get('1.0','end-1c'))
        print(output_entry.get())
        if option.get() == "Image":
            lsb_encode(entry_path.get(), entry_message.get('1.0','end-1c'), output_entry.get())
        else:
            print('audio')

    button_encode = Button(tab1, text='Hide message', width=25,
                    height=1, bg=bg_color, borderwidth=2, command=handle_encode)
    button_encode.place(x=110, y=290)

    # Decode process
    # File path process
    file_path_text = Label(tab2, font=(text_style, text_size),text='File path:', bg=bg_color)
    file_path_text.place(x=30, y=30)

    entry_path = Entry(tab2, width=45, font=(text_style, text_size))
    entry_path.place(x=110, y=30)

    def browsefunc_input():
        cur_dir = os.getcwd()
        input_path = filedialog.askopenfilename(
            initialdir=cur_dir, title='Select file')
        entry_path.insert(END, input_path)  # add this

    button_tab2 = Button(tab2, text='Browse', width=5,
                    height=1, bg=bg_color, borderwidth=2, command=browsefunc_input)
    button_tab2.place(x=580, y=28)

    option = StringVar(tab2)
    option.set("Image") # default value

    w = OptionMenu(tab2, option, "Image", "Audio")
    w.pack(expand=True)
    w.place(x=400, y=80)

    def handle_decode():
        if option.get() == "Image":
            decoded = lsb_decode(entry_path.get())
            result_text = Label(tab2, font=(text_style, text_size), text='Result: ' + decoded, bg='red')
            result_text.place(x=30, y=150)
        else:
            print('audio')

    button_decode = Button(tab2, text='Reveal message', width=25,
                    height=1, bg=bg_color, borderwidth=2, command=handle_decode)
    button_decode.place(x=110, y=80)

    win.mainloop()

if __name__ == "__main__":
    application()