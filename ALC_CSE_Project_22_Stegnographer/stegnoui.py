from tkinter import *
import PIL.Image
from tkinter.filedialog import *
from tkinter import filedialog
import os
from PIL import ImageTk as itk
from tkinter import messagebox

MAX_COLOR_VALUE = 256
MAX_BIT_VALUE = 8
size = 1920, 1080
# size = 2560, 1440
dir1 = ""
dir2 = ""


def make_image(data, resolution):
    image = PIL.Image.new("RGB", resolution)
    image.putdata(data)

    return image


def remove_n_least_significant_bits(value, n):
    value = value >> n
    return value << n


def get_n_least_significant_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOR_VALUE
    return value >> MAX_BIT_VALUE - n


def get_n_most_significant_bits(value, n):
    return value >> MAX_BIT_VALUE - n


def shit_n_bits_to_8(value, n):
    return value << MAX_BIT_VALUE - n


def encode(image_to_hide, image_to_hide_in, n_bits):
    width, height = image_to_hide.size

    hide_image = image_to_hide.load()
    hide_in_image = image_to_hide_in.load()

    data = []


    for y in range(height):
        for x in range(width):
             # (107, 3, 10)
             # most sig bits
            try:
                pixel = hide_image[x, y]
                r_hide, g_hide, b_hide = pixel[0], pixel[1], pixel[2]

                

                r_hide = get_n_most_significant_bits(r_hide, n_bits)
                g_hide = get_n_most_significant_bits(g_hide, n_bits)
                b_hide = get_n_most_significant_bits(b_hide, n_bits)

              # remove lest n sig bits 
                pixel_in = hide_in_image[x, y]
                r_hide_in, g_hide_in, b_hide_in = pixel_in[0], pixel_in[1], pixel_in[2]

                
                    

                r_hide_in = remove_n_least_significant_bits(r_hide_in, n_bits)
                g_hide_in = remove_n_least_significant_bits(g_hide_in, n_bits)
                b_hide_in = remove_n_least_significant_bits(b_hide_in, n_bits)

                data.append((r_hide + r_hide_in,
                             g_hide + g_hide_in,
                             b_hide + b_hide_in))
                

            except:
                continue

    return make_image(data, image_to_hide.size)


def decode(image_to_decode, n_bits):
    width, height = image_to_decode.size
    encoded_image = image_to_decode.load()

    data = []

    for y in range(height):
        for x in range(width):
            r_encoded, g_encoded, b_encoded = encoded_image[x, y]

            r_encoded = get_n_least_significant_bits(r_encoded, n_bits)
            g_encoded = get_n_least_significant_bits(g_encoded, n_bits)
            b_encoded = get_n_least_significant_bits(b_encoded, n_bits)

            r_encoded = shit_n_bits_to_8(r_encoded, n_bits)
            g_encoded = shit_n_bits_to_8(g_encoded, n_bits)
            b_encoded = shit_n_bits_to_8(b_encoded, n_bits)

            data.append((r_encoded, g_encoded, b_encoded))

    return make_image(data, image_to_decode.size)


def upload_container_img():
    try:
        global dir1

        directory = str(askopenfile())
        dir1_ins1 = directory.index("name='")
        dir1_ins2 = directory.index("'", dir1_ins1+7)
        dir1 = directory[dir1_ins1+6:dir1_ins2]
    except Exception as e:
        print(str(e))
        messagebox.showinfo(
            "Error",  "Some Error Occured, Kindly reopen the app and control as per instructions")
        window.destroy()


def upload_box_img():
    try:
        global dir2

        directory = str(askopenfile())
        dir2_ins1 = directory.index("name='")
        dir2_ins2 = directory.index("'", dir2_ins1+7)
        dir2 = directory[dir2_ins1+6:dir2_ins2]

    except Exception as e:
        print(str(e))
        messagebox.showinfo(
            "Error",  "Some Error Occured, Kindly reopen the app and control as per instructions")
        window.destroy()


def encode_start():
    try:
        global dir1
        global dir2

        n_bits = 2

        # box = secret
        # container = cover
        box_image_path = str(dir2)
        container_image_path = str(dir1)
        path_dir1 = dir1.rfind('/')
        encoded_image_path = dir1[:path_dir1]+"/encoded.tiff"
        print(encoded_image_path)
        box_image = PIL.Image.open(mode='r', fp=box_image_path)
        container_image = PIL.Image.open(mode='r', fp=container_image_path)

        encode(box_image, container_image, n_bits).save(encoded_image_path)
        messagebox.showinfo(
            "Complete",  "Encryption Succesfull - encoded.tiff")
        dir1 = ""
        dir2 = ""

    except Exception as e:
        print(str(e))
        messagebox.showinfo(
            "Error",  "Some Error Occured, Kindly reopen the app and control as per instructions")
        window.destroy()


def decode_start():
    try:
        global newWindow
        global dir1
        path_dir1 = dir1.rfind('/')
        decoded_image_path = dir1[:path_dir1]+"/Decoded.tiff"
        encoded_image_path = str(dir1)
        n_bits = 2
        image_to_decode = PIL.Image.open(mode='r', fp=encoded_image_path)
        decode(image_to_decode, n_bits).save(decoded_image_path)
        messagebox.showinfo(
            "Complete",  "Decryption Succesfull - Decoded.tiff")

    except Exception as e:
        print(str(e))
        messagebox.showinfo(
            "Error",  "Some Error Occured, Kindly reopen the app and control as per instructions")
        window.destroy()


def upload_img_decode():
    try:
        global dir1

        directory = str(askopenfile())
        dir1_ins1 = directory.index("name='")
        dir1_ins2 = directory.index("'", dir1_ins1+7)
        dir1 = directory[dir1_ins1+6:dir1_ins2]

    except Exception as e:
        print(str(e))
        messagebox.showinfo(
            "Error",  "Some Error Occured, Kindly reopen the app and control as per instructions")
        window.destroy()


def test_clicked():
    print("test Clicked")


window = Tk()

window.geometry("894x678")
window.configure(bg="#ffffff")
window.title('Steganographer')
canvas = Canvas(
    window,
    bg="#ffffff",
    height=678,
    width=894,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

# background_img = PhotoImage(file=f"background.png")
background_img = PhotoImage(file=f"bg_try2.png")
background = canvas.create_image(
    447.0, 336.0,
    image=background_img)

img0 = PhotoImage(file=f"img0.png")
btn_decrypt = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=decode_start,
    relief="flat")

btn_decrypt.place(
    x=400, y=388,
    width=92,
    height=47)

img1 = PhotoImage(file=f"img1.png")
btn_encrypt = Button(
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=encode_start,
    relief="flat")

btn_encrypt.place(
    x=401, y=238,
    width=92,
    height=47)

img2 = PhotoImage(file=f"img2.png")
btn_decrypt_input = Button(
    image=img2,
    borderwidth=0,
    highlightthickness=0,
    command=upload_img_decode,
    relief="flat")

btn_decrypt_input.place(
    x=500, y=374,
    width=195,
    height=73)

img3 = PhotoImage(file=f"img41.png")
btn_container = Button(
    image=img3,
    borderwidth=0,
    highlightthickness=0,
    command=upload_container_img,
    relief="flat")

btn_container.place(
    x=263, y=276,
    width=137,
    height=61)

img4 = PhotoImage(file=f"img31.png")
btn_box = Button(
    image=img4,
    borderwidth=0,
    highlightthickness=0,
    command=upload_box_img,
    relief="flat")

btn_box.place(
    x=262, y=196,
    width=137,
    height=64)

window.resizable(False, False)
window.mainloop()
