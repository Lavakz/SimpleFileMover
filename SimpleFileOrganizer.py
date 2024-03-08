import os
import subprocess
import random
import shutil
import sys

dir_filename = "dirs.txt"
file_types = (".jpg", ".png")
files = {}
fav_dirs = []
batch_move = False

windows = False
linux_image_viewer = "chafa"


class Random_File:
    def __init__(self, file_dir=""):
        self.dir: str = (
            random.choice(list(files.keys())) if file_dir == "" else fav_dirs[file_dir]
        )
        files_in_dir = os.listdir(self.dir)
        if not files_in_dir:
            print("No more files to move...")
            return
        self.file: str = random.choice(files_in_dir)
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
        for fav_i, fav_dir in enumerate(fav_dirs):
            print(f"{fav_i+1}) {fav_dir}")
        feedback: str = input(f"Move to... (1-{len(fav_dirs)}): ")
        rating: int = (
            int(-1 if feedback == "" or not feedback.isdigit() else feedback)
        ) - 1
        if 0 <= rating and rating < len(fav_dirs):
            new_path: str = fav_dirs[rating]
        else:
            new_path: str = "not moved"

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
            subprocess.call([linux_image_viewer, self.path])
        print(f"{self.file} in {self.dir}")
        return

    def move(self, new_path):
        if new_path == "not moved":
            print("file not moved")
            return
        shutil.move(self.path, new_path)
        print(f"Moved {self.file} to {new_path}")


def get_files(file_dir, overwrite=False):
    if len(files[file_dir]) == 0 or overwrite:  # scan dir if not already scanned
        files[file_dir] = [
            file for file in os.listdir(file_dir) if file.endswith(file_types)
        ]
    return files[file_dir]


def get_input(prompt="-> "):
    selection = input(prompt)
    if selection.isdigit() == False:
        return get_input("Not a valid selection\n-> ")
    return int(selection)


def get_info():
    for d, f in files.items():  # scan all dirs
        f = get_files(d, True)
    print("\nUnorganized Folders:")
    for i, file_dir in enumerate(list(files.keys())):
        print(f"{i+1}) {len(get_files(file_dir))} files in {file_dir}")
    print("\nOrganized Folders:")
    for i, file_dir in enumerate(fav_dirs):
        print(f"{i+1}) {len(os.listdir(file_dir))} files in {file_dir}")


def get_dirs():
    with open(dir_filename, "r") as file:
        dir_names = [
            line.rstrip() for line in file.readlines() if not line.startswith("#")
        ]
        for i in range(dir_names.index("unorganized:") + 1, len(dir_names)):
            if dir_names[i] != "":
                files[dir_names[i]] = []
            else:
                break
        for i in range(dir_names.index("organized:") + 1, len(dir_names)):
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
        "Move Files",
        "Open Random Organized File",
        "Open Random Unorganized File",
        "Get Info",
        "Quit",
    ]
    for i, item in enumerate(menu):
        print("%d) %s" % (i + 1, item))

    match get_input():
        case 1:
            if len(fav_dirs) == 0:
                print("No organized directories found")
            else:
                count = input("\nHow many files to move?\n-> ")
                if count == "":
                    count = "1"
                if count.isdigit() == True:
                    Random_File().rate(0, int(count if int(count) > 0 else 1))
        case 2:
            rating = int(input("\nWhich directory?\n-> "))
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
