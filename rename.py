from threading import Thread
import os


def rename_files(directory):
    i = 1
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".gif"):
            new_name = str(i) + ".gif"
            os.rename(os.path.join(directory, filename),
                      os.path.join(directory, new_name))
            print(f"Renamed {filename} to {new_name}")
            i += 1


currentdir = os.path.dirname(os.path.abspath(__file__))

directory = currentdir
t = Thread(target=rename_files, args=(directory,))
t.start()
