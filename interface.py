from tkinter import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import os
from core import *
from configs import *
from audio import *
from ccrypt import *
import utils

# constants
bg_color = '#E0E0E0'
text_style = 'Segoe UI'
text_size = 12
text_color = '#3030303'
padX = 10
padY = 8

revealed_message = ''

def setEntryText(entry, text): 
    entry.delete(0, END)
    entry.insert(0, text)

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

    ## Tab 1
    # File path process
    t1_input_path_label = Label(tab1, font=(text_style, text_size),text='Cover file:', bg=bg_color)
    t1_input_path_label.place(x=30, y=30)

    t1_input_path = Entry(tab1, width=45, font=(text_style, text_size))
    t1_input_path.place(x=110, y=30)

    def browsefunc_input():
        cur_dir = os.getcwd()
        input_path = filedialog.askopenfilename(
            initialdir=cur_dir, title='Select file')
        setEntryText(t1_input_path, input_path)  # add this

    t1_browse_input_button = Button(tab1, text='Browse', width=5,
                    height=1, bg=bg_color, borderwidth=2, command=browsefunc_input)
    t1_browse_input_button.place(x=580, y=28)

    # Message process
    t1_secret_message_label = Label(tab1, font=(text_style, text_size), text='Message:', bg=bg_color)
    t1_secret_message_label.place(x=30, y=80)

    t1_secret_message = Text(tab1, width=56, height=6)
    t1_secret_message.place(x=110, y=80)    

    # Password
    t1_password_label = Label(tab1, font=(text_style, text_size), text='Password:', bg=bg_color)
    t1_password_label.place(x=30, y=205)

    t1_password = Entry(tab1, width=45, font=(text_style, text_size))
    t1_password.place(x=110, y=205)

    # Output process
    t1_output_folder_label = Label(tab1, font=(text_style, text_size), text='Output:', bg=bg_color)
    t1_output_folder_label.place(x=30, y=250)

    t1_output_folder = Entry(tab1, width=45, font=(text_style, text_size))
    t1_output_folder.place(x=110, y=250)

    def browsefunc_output():
        cur_dir = os.getcwd()
        tmp = filedialog.askdirectory(
            initialdir=cur_dir, title='Select directory')
        setEntryText(t1_output_folder, tmp)  # add this

    t1_browse_output_button = Button(tab1, text='Browse', width=5,
                    height=1, bg=bg_color, borderwidth=2, command=browsefunc_output)
    t1_browse_output_button.place(x=580, y=248)

    # Encode process
    t1_file_type_option = StringVar(tab1)
    t1_file_type_option.set("Image") # default value

    w = OptionMenu(tab1, t1_file_type_option, "Image", "Audio", command=lambda selection: t1_file_type_option.set(selection))
    w.pack(expand=True)
    w.place(x=400, y=290)

    def handle_encode():
        file_type = t1_file_type_option.get()
        inp = t1_input_path.get()
        msg = t1_secret_message.get('1.0', 'end-1c')
        password = t1_password.get()
        outp = t1_output_folder.get()

        # encrypt message
        if password:
            msg = CCrypt.encode(msg, password)
            print(msg)

        if not inp or not os.path.exists(inp):
            messagebox.showerror('Error', 'Invalid input path: ' + inp)
            return
        if utils.get_file_extension(inp) is None or utils.get_file_extension(inp) not in SupportedFileExts[file_type]:
            messagebox.showerror('Error', f'Unsupported file type: {utils.get_file_extension(inp)}. Please use files with the following extensions: {", ".join(SupportedFileExts[file_type])}')
            return
        
        if not msg or len(msg) == 0:
            messagebox.showerror('Missing parameter', 'Secret text required')
            return

        if not os.path.exists(outp):
            messagebox.showerror('Error', 'Invalid output path: ' + outp)
            return
        
        outp_file = ''
        if file_type == 'Image':
            outp_file = os.path.join(outp, os.path.basename(inp).removesuffix(f'.{utils.get_file_extension(inp)}') + '_with_message.png')
            try:
                success, message = lsb_encode(inp, msg, outp_file)
                if success:
                    messagebox.showinfo('Success', message)
                else:
                    messagebox.showerror('Error', message)
            except Exception as e:
                messagebox.showerror('Error', str(e))
                return
        elif file_type == 'Audio':
            outp_file = os.path.join(outp, os.path.basename(inp).removesuffix(f'.{utils.get_file_extension(inp)}') + '_with_message.wav')
            try:
                sample_rate, data, n_samples, n_channels = AudioSteg.wav_data(inp)
                success, message = AudioSteg.LSB.encode(data, msg, channels=[0])
                if not success:
                    messagebox.showerror('Error', message)
                    return
                else:
                    AudioSteg.save_wav(sample_rate, data, outp_file)
                    messagebox.showinfo('Success', message + ': ' + outp_file)                    
            except Exception as e:
                messagebox.showerror('Error', str(e))
                return
        


    button_encode = Button(tab1, font=(text_style, text_size), text='Hide message', width=25,
                    height=1, bg=bg_color, borderwidth=2, command=handle_encode)
    button_encode.place(x=110, y=290)



    ## Tab 2
    # Decode process
    # File path process
    t2_input_path_label = Label(tab2, font=(text_style, text_size),text='Cover file:', bg=bg_color)
    t2_input_path_label.place(x=30, y=30)

    t2_input_path = Entry(tab2, width=45, font=(text_style, text_size))
    t2_input_path.place(x=110, y=30)

    # Password
    t2_password_label = Label(tab2, font=(text_style, text_size), text='Password:', bg=bg_color)
    t2_password_label.place(x=30, y=80)

    t2_password = Entry(tab2, width=45, font=(text_style, text_size))
    t2_password.place(x=110, y=80)

    t2_output_message_label = Label(tab2, font=(text_style, text_size), text='Message:', bg=bg_color)
    t2_output_message_label.place(x=30, y=130)

    t2_output_message = Entry(tab2, width=45, font=(text_style, text_size))
    t2_output_message.place(x=110, y=130)

    def t2_browsefunc_input():
        cur_dir = os.getcwd()
        tmp = filedialog.askopenfilename(
            initialdir=cur_dir, title='Select file')
        setEntryText(t2_input_path, tmp)  # add this

    button_tab2 = Button(tab2, text='Browse', width=5,
                    height=1, bg=bg_color, borderwidth=2, command=t2_browsefunc_input)
    button_tab2.place(x=580, y=30)

    t2_file_type_option = StringVar(tab2)
    t2_file_type_option.set("Image") # default value

    w2 = OptionMenu(tab2, t2_file_type_option, "Image", "Audio",
                   command=lambda selection: t2_file_type_option.set(selection))
    w2.pack(expand=True)
    w2.place(x=400, y=160)

    def handle_decode():
        file_type = t2_file_type_option.get()
        inp = t2_input_path.get()
        password = t2_password.get()

        if not inp or not os.path.exists(inp):
            messagebox.showerror('Error', 'Invalid input path: ' + inp)
            return
        if utils.get_file_extension(inp) is None or utils.get_file_extension(inp) not in SupportedFileExts[file_type]:
            messagebox.showerror('Error', f'Unsupported file type: {utils.get_file_extension(inp)}. Please use files with the following extensions: {", ".join(SupportedFileExts[file_type])}')
            return
        
        if file_type == "Image":
            try: 
                decoded = lsb_decode(inp)
                if password:
                    success, decrypted = CCrypt.decode(decoded, password)
                    if success:
                        setEntryText(t2_output_message, decrypted)
                    else:
                        messagebox.showerror('Error', 'Invalid password')
                else:
                    setEntryText(t2_output_message, decoded)
            except Exception as e:
                messagebox.showerror('Error', str(e))
        elif file_type == "Audio":
            try:
                _, data, _, _ = AudioSteg.wav_data(inp)
                res = AudioSteg.LSB.decode(data, channels=[0])
                if password:
                    success, decrypted = CCrypt.decode(res[0], password)
                    if success:
                        setEntryText(t2_output_message, decrypted)
                    else:
                        messagebox.showerror('Error', 'Invalid password')
                else:
                    setEntryText(t2_output_message, res[0])
            except Exception as e:
                messagebox.showerror('Error', str(e))
    button_decode = Button(tab2, text='Reveal message', width=25,
                    height=1, bg=bg_color, borderwidth=2, command=handle_decode)
    button_decode.place(x=110, y=160)

    win.mainloop()

if __name__ == "__main__":
    application()