import os
import sys
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
pic_path = os.path.join(script_dir, 'pic')

class ImageConverter:

    def __init__(self):
        self.input_directory = pic_path


    def process_image(self, file_name):
        img_path = os.path.join(self.input_directory, file_name)
        self.resize_image(img_path)
            

    # Resize the image given by input_path and overwrite to the same path
    def resize_image(self, img_path):
        # Screen target size dims
        target_width = 600
        target_height = 448

        with Image.open(img_path) as img:
            img = ImageOps.exif_transpose(img)
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
            
            # Original dimensions
            orig_width, orig_height = img.size

            original_aspect_ratio = orig_width / orig_height
            target_aspect_ratio = target_width / target_height

            # Fit height and crop sides
            if original_aspect_ratio > target_aspect_ratio:
                new_height = target_height
                new_width = int(new_height * original_aspect_ratio)
            # Fit width and crop top/bottom
            else:
                new_width = target_width
                new_height = int(new_width / original_aspect_ratio)

            # Resize the image while maintaining aspect ratio
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Calculate the cropping box to center the crop
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height

            # Crop the image
            cropped_img = resized_img.crop((left, top, right, bottom))

            # Save the final image
            cropped_img.save(img_path)
