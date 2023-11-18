from PIL import Image
import os
from send2trash import send2trash


def entry():
    header_art = ""
    running = True
    while running:
        print("ENTRY START")
        menu_choice_valid = False
        while not menu_choice_valid:
            menu_choice = input(
                "1. Rotate Images\n"
                "2. Flip Images\n"
                "q. quit\n"
            ).strip()
            if menu_choice[0] == "1" or menu_choice[0] == "2" or menu_choice[0] == "q":
                menu_choice_valid = True
            else:
                print("Invalid selection")
            if menu_choice[0] == "q":
                return

        # Get directory
        folder_input_path = input("Enter filepath to folder...\n").strip()
        if os.path.isdir(folder_input_path):
            source_path = folder_input_path
        else:
            print("invalid filepath, try again.")
            return

        # Source or New Folder?
        folder_decision_valid = False
        while not folder_decision_valid:
            folder_decision = input("1. Replace original images with changes.\n"
                                    "2. Replace original images and move to new folder within current dir\n"
                                    "3. Keep original, changes move to separate folder within current dir\n").strip()
            if folder_decision == "1" or folder_decision == "2" or folder_decision == "3":
                folder_decision_valid = True

        # make new dir
        if folder_decision == "2" or folder_decision == "3":
            target_dir_name = input("Name your new folder:\n")
            target_dir_path = os.path.join(source_path, target_dir_name)
            os.mkdir(target_dir_path)

        match folder_decision:
            case "1":
                # No changing functions...
                mode = 1
            case "2":
                # New folder with OG img replaced
                mode = 2
            case "3":
                # Preserve OG imgs, new folder with resulting operation
                mode = 3

        match menu_choice:
            case "1":
                if mode != 1:
                    rotate_images(source_path, target_dir_path, mode)
                else:
                    rotate_images(source_path, None, mode)
            case "2":
                if mode != 1:
                    flip_images(source_path, target_dir_path, mode)
                else:
                    flip_images(source_path, None, mode)
            case _:
                print("If you see this, the switch case in entry is broken.")


def rotate_images(source_dir: str, target_dir, mode: int):
    # Mode arg refers to folder decision in entry()

    degree_change: float = 90
    print("1. Rotate clockwise 90 degrees\n2. Rotate counter-clockwise 90 degrees\n")
    # ----------------------------------------------------------------------------------ADD: input validating
    rotation_direction_input = input()

    if rotation_direction_input == "1":
        degree_change *= -1.0

    # going through files in source dir
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if not os.path.isdir(file_path):
            try:
                with Image.open(file_path) as image:
                    rotated_image = image.rotate(degree_change, expand=True)
                    # MODE STUFF
                    if not mode or mode == 1:
                        rotated_image.save(file_path)
                    if mode == 2 or mode == 3:
                        new_file_path = os.path.join(target_dir, file_name)
                    if mode == 2:
                        # Replace (duplicate and delete OG) original images and create folder within current dir
                        rotated_image.save(new_file_path)
                    elif mode == 3:
                        # Do not replace original, separate folder within current dir
                        rotated_image.save(new_file_path)

            except Exception as e:
                print("Image files failed to open...", e)
    # deleting image files if mode 2 or 3
    if mode == 2 or mode == 3:
        for item in os.listdir(source_dir):
            item_path = os.path.join(source_dir, item)
            if not os.path.isdir(item_path):
                send2trash(item_path)

    print("Returning to Menu.")


def flip_images(source_dir: str, target_dir, mode: int):
    flip_direction_input_valid = False
    while not flip_direction_input_valid:
        print("1. Flip horizontally\n2. Flip vertically")
        flip_direction_input = input().strip()
        if flip_direction_input == "1" or flip_direction_input == "2":
            flip_direction_input_valid = True
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if not os.path.isdir(file_path):
            try:
                with Image.open(file_path) as image:
                    if flip_direction_input == "1":
                        # 0 in argument is Transpose.FLIP_LEFT_RIGHT (pillow builtin)
                        flipped_image = image.transpose(0)
                    if flip_direction_input == "2":
                        # 1 in arg is FLIP_TOP_BOTTOM
                        flipped_image = image.transpose(1)

                    # MODE STUFF
                    if mode == 2 or mode == 3:
                        new_file_path = os.path.join(target_dir, file_name)
                    if mode == 2:
                        # Replace (duplicate and delete OG) original images and create folder within current dir
                        flipped_image.save(new_file_path)
                    elif mode == 3:
                        # Do not replace original, separate folder within current dir
                        flipped_image.save(new_file_path)
                    else:
                        # Mode 1 or no mode
                        flipped_image.save(file_path)
            except Exception as e:
                print("Image files failed to open...", e)
    if mode == 2:
        for item in os.listdir(source_dir):
            item_path = os.path.join(source_dir, item)
            if not os.path.isdir(item_path):
                send2trash(item_path)

    print("Returning to Menu.")


def print_head():
    line = ["                    .@@@@@ @@@@@@@@@@                    ",
            "                   @@@@@@@@..@@@@@@@@@                   ",
            "                  @@@@@@@@@@ .@@@@@@@@@                  ",
            "                 @@@@@@@@@@   .@@@@@@@@@@                ",
            "                  @@@@@@@@      @@@@@@@.                 ",
            "                     -@@@     @@@@@@@@.                  ",
            "            @@@@@@@@                    @@@=             ",
            "             @@@@@@@@                @@@@@@@@            ",
            "            @@@@@@@@@.              @@@@@@@@@@           ",
            "           @@@@@@@@@@@               @@@@@@@@@.          ",
            "           @@@@@@@@@ @                @@@@@@@@           ",
            "            @@@@@@@              @     @@@@@@            ",
            "             @@@@:  .           @@+:    .  @@            ",
            "              @@ .@@@@@@@@@    @@@@@@@@@@@@@             ",
            "               @ @@@@@@@@@@  @@@@@@@@@@@@@@              ",
            "                 @@@@@@@@@@   @@@@@@@@@@@@               ",
            "                 .@@@@@@@@@    @@@@@@@@@@                ",
            "                                @@                       ",
            "                                 @                        "]

    for i in line:
        print(i)


print_head()
entry()
