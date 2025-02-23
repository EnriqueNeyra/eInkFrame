import os
import sys
import time
import random
from PIL import Image, ImageDraw, ImageEnhance
from io import BytesIO
import socket
import qrcode

# Automatically add the 'lib' directory relative to the script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(SCRIPT_DIR, 'lib')
PIC_PATH = os.path.join(SCRIPT_DIR, 'pic')
sys.path.append(LIB_PATH)
from lib.waveshare_epd import epd5in65f

class Display:

    def __init__(self):
        self.last_display_time = time.time()
        self.last_selected_image = None
        self.rotation = 0
        self.epd = epd5in65f.EPD()
        self.epd.init()


    def fetch_image_files(self):
        return [f for f in os.listdir(PIC_PATH)]


    def select_random_image(self, images):
        # If one image or less
        if len(images) <= 1:
            return images[0]
        
        # Select a random image unless it was previously selected
        random_image = random.choice([img for img in images if img != self.last_selected_image and img != "qrcode.bmp"])
        
        return random_image


    def clear_display(self):
        self.epd.init()
        self.epd.Clear()


    def display_image(self, img = None):
        self.epd.init()
        
        if img:
            self.last_selected_image = img
            pic_path = os.path.join(PIC_PATH, img)
            
            # Open and display the image
            with Image.open(pic_path) as pic:
                pic = pic.rotate(self.rotation)
                self.epd.display(self.epd.getbuffer(pic))
                self.last_display_time = time.time()
        
        else:
            images = self.fetch_image_files()
            random_image = self.select_random_image(images)
            self.last_selected_image = random_image
            
            # Open and display the image
            with Image.open(os.path.join(PIC_PATH, random_image)) as pic:
                pic = pic.rotate(self.rotation)
                self.epd.display(self.epd.getbuffer(pic))
                self.last_display_time = time.time()

        while True:
            current_time = time.time()
            elapsed_time = current_time - self.last_display_time
            
            if elapsed_time >= 360:
                images = self.fetch_image_files()
                random_image = self.select_random_image(images)
                self.last_selected_image = random_image

                # Open and display the image
                with Image.open(os.path.join(PIC_PATH, random_image)) as pic:
                    pic = pic.rotate(self.rotation)
                    self.epd.display(self.epd.getbuffer(pic))
                    self.last_display_time = time.time()
    
    def display_qrcode(self, ip_address):
        url = f"http://{ip_address}:5000"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create QR Code BMP
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_img = qr_img.resize((300, 300))
        
        full_img = Image.new("RGB", (600, 448), color="white")

        qr_x = (full_img.width - qr_img.width) // 2
        qr_y = (full_img.height - qr_img.height) // 2
        full_img.paste(qr_img, (qr_x, qr_y))
        
        full_img.save(os.path.join(PIC_PATH, "qrcode.bmp"), format = "BMP")
        with Image.open(os.path.join(PIC_PATH, "qrcode.bmp")) as bmp_qr:
            bmp_qr = bmp_qr.rotate(self.rotation)
            self.epd.display(self.epd.getbuffer(bmp_qr))




