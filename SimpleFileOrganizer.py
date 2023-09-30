import os
import subprocess
import random
import shutil
import sys

dir_filename = "dirs.txt"
files = {}
fav_dirs = []
batch_move = False

windows = False
image_viewer = "feh"


class Random_File:
    def __init__(self, dir=""):
        self.dir: str = (
            random.choice(list(files.keys())) if dir == "" else fav_dirs[dir]
        )
        self.file: str = random.choice(os.listdir(self.dir))
        self.path: str = f"{self.dir}/{self.file}"

    def rate(self, i=0, count=1):
        """
        Rate a random file and move it to a favorite directory
        Loop until i is equal to count
        """
        if i >= count:
            return
        print(f"\n\b[ {i+1} / {count} ]")
        self.open()
        feedback: str = input(f"Rating (1-{len(fav_dirs)}): ")
        rating: int = int(-1 if feedback == "" or not feedback.isdigit() else feedback)
        if 0 < rating and rating < len(fav_dirs) - 1:
            new_path: str = fav_dirs[rating - 1]
        else:
            new_path: str = "no rating"

        if batch_move:
            Random_File().rate(i + 1, count)
            self.move(new_path)
        else:
            self.move(new_path)
            Random_File().rate(i + 1, count)

    def open(self):
        if windows:
            os.startfile(self.path)
        else:
            subprocess.call([image_viewer, self.path])
        print(f"Opened {self.file} in\n{self.dir}\n")
        return

    def move(self, new_path):
        if new_path == "no rating":
            print("No rating given")
            return
        shutil.move(self.path, new_path)
        print(f"Moved {self.file} to {new_path}")


def get_files(dir, overwrite=False):
    if len(files[dir]) == 0 or overwrite:  # scan dir if not already scanned
        files[dir] = [
            file for file in os.listdir(dir) if file.endswith((".mp4", ".mkv", ".webm"))
        ]
    return files[dir]


def get_input(prompt="-> "):
    selection = input(prompt)
    if selection.isdigit() == False:
        return get_input("Not a valid selection\n-> ")
    return int(selection)


def get_info():
    for d, f in files.items():  # scan all dirs
        f = get_files(d, True)
    print("\nUnrated Folders:")
    for i, dir in enumerate(list(files.keys())):
        print(f"{i+1}) {len(get_files(dir))} files in {dir}")
    print("\nRated Folders:")
    for i, dir in enumerate(fav_dirs):
        print(f"{i}) {len(os.listdir(dir))} files in {dir}")


def get_dirs():
    with open(dir_filename, "r") as file:
        dir_names = [
            line.rstrip() for line in file.readlines() if not line.startswith("#")
        ]
        for i in range(dir_names.index("unrated:") + 1, len(dir_names)):
            if dir_names[i] != "":
                files[dir_names[i]] = []
            else:
                break
        for i in range(dir_names.index("rated:") + 1, len(dir_names)):
            if dir_names[i] != "":
                fav_dirs.append(dir_names[i])
            else:
                break


def main():
    if len(files) == 0:
        print("No directory paths in this file")
        sys.exit()

    print("\n\bMain Menu:")
    menu = [
        "Rate Files",
        "Open Random Rated File",
        "Open Random Unrated File",
        "Get Info",
        "Quit",
    ]
    for i, item in enumerate(menu):
        print("%d) %s" % (i + 1, item))

    match get_input():
        case 1:
            if len(fav_dirs) == 0:
                print("No favorite directories found")
            else:
                count = input("\nHow many files to rate?\n-> ")
                if count == "":
                    count = "1"
                if count.isdigit() == True:
                    Random_File().rate(0, int(count if int(count) > 0 else 1))
        case 2:
            rating = int(input("\nWhat rating?\n-> "))
            Random_File(rating).open()
            while input(f"Open another file in {fav_dirs[rating]}? (y/n)\n-> ") != "n":
                Random_File(rating).open()
        case 3:
            Random_File().open()
            while input("Open another file? (y/n)\n-> ") != "n":
                Random_File().open()
        case 4:
            get_info()
        case 5:
            sys.exit()
        case _:
            main()

    main()


if __name__ == "__main__":
    print("\nSimple File Organizer")
    get_dirs()
    get_info()
    main()
