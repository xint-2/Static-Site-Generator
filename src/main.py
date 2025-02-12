from textnode import TextNode, TextType
import os
import shutil

def recursive_copier(source_directory, static_site_directory):
    items = os.listdir(source_directory)

    if not os.path.exists(static_site_directory):
        os.mkdir(static_site_directory)

    for item in items:
        full_path = os.path.join(source_directory, item)
        static_path = os.path.join(static_site_directory, item)

        if os.path.isfile(full_path):
            print(f"Copying file: {full_path} -> {static_path}")
            shutil.copy(full_path, static_path)
        
        elif os.path.isdir(full_path):
            print(f"Creating Directory: {static_path}")
            if not os.path.exists(static_path):
                os.mkdir(static_path)
            recursive_copier(full_path, static_path)
            
def main():
    source_directory = "/home/tjm/public/static"
    static_site_directory = "/home/tjm/public/static_site"

    recursive_copier(source_directory, static_site_directory)


main()
