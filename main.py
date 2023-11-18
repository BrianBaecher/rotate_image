from PIL import Image
import os


def rotate_image():
    running = True
    while running:
        degree_change: float = 90
        folder_input_path = input("Enter filepath to folder... Or enter N/n to quit\n").strip()
        if folder_input_path.lower() == "n":
            running = False
            print("Exiting...")
        if not running:
            return
        if os.path.isdir(folder_input_path):
            folder_path = folder_input_path
        else:
            print("invalid filepath, try again.")
            return
        print("1. Rotate clockwise 90 degrees\n2. Rotate counter-clockwise 90 degrees\n3. Quit.")
        rotation_direction_input = input()
        if rotation_direction_input == "1":
            degree_change *= -1.0
        if rotation_direction_input == "3":
            running = False
        if not running:
            print("Exiting...")
            return
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                with Image.open(file_path) as image:
                    rotated_image = image.rotate(degree_change, expand=True)
                    rotated_image.save(file_path)
            except Exception as e:
                print("Image files failed to open...", e)
        repeat_input_processed = False
        while not repeat_input_processed:
            repeat_input = input("Repeat Process? \n1. Yes\n2. No\n").strip()
            if repeat_input == "1":
                repeat_input_processed = True
                continue
            if repeat_input == "2":
                repeat_input_processed = True
                running = False
                print("Bye.")


rotate_image()
