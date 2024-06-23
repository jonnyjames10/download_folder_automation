from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move, unpack_archive
import zipfile
import time

import logging

from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler # type: ignore

# NEED TO MAKE SURE TO USE DOUBLE BACK SLASHES
source_dir = "C:\\Users\\jonny\\Downloads\\test_move_folder"
dest_music_dir = "C:\\Users\\jonny\\Music\\downloads_go_here"
dest_image_dir = "C:\\Users\\jonny\\OneDrive\\Pictures\\downloads_go_here"
dest_document_dir = "C:\\Users\\jonny\\OneDrive\\Documents"
dest_video_dir = "C:\\Users\\jonny\\Videos\\Downloaded videos"
dest_zip_file = "C:\\Users\\jonny\\Downloads\\ZIP Files"

music_file_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.alac', '.aiff', '.aif', '.aifc', '.opus', '.mp2', '.mka', '.mid', '.midi', '.rmi']
image_file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico', '.heic', '.heif', '.raw', '.cr2', '.nef', '.orf', '.sr2', '.psd', '.ai', '.eps']
video_file_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2', '.ogv', '.rm', '.rmvb', '.vob', '.ts', '.m2ts', '.mxf', '.divx']
document_file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']

#TODO: Create function to rename file if already exists in destination folder

def move_file(destination, file, name):
    filename, extension= splitext(name)
    # if exists(destination):
    #    pass
    move(file, destination)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for ent in entries: # GO THROUGH EACH FILE
                name = ent.name
                self.move_music_file(ent, name)
                self.move_image_file(ent, name)
                self.move_video_file(ent, name)
                self.move_doc_file(ent, name)
                self.unzip_folder(ent, name)
    
    def move_music_file(self, file, name):
        for e in music_file_extensions:
            if name.endswith(e) or name.endswith(e.upper()):
                move_file(dest_music_dir, file, name)
                logging.info(f"Moved music file: {name}")
    
    def move_image_file(self, file, name):
        for e in image_file_extensions:
            if name.endswith(e) or name.endswith(e.upper()):
                move_file(dest_image_dir, file, name)
                logging.info(f"Moved image file: {name}")
    
    def move_video_file(self, file, name):
        for e in video_file_extensions:
            if name.endswith(e) or name.endswith(e.upper()):
                move_file(dest_video_dir, file, name)
                logging.info(f"Moved video file: {name}")
    
    def move_doc_file(self, file, name):
        for e in document_file_extensions:
            if name.endswith(e) or name.endswith(e.upper()):
                move_file(dest_document_dir, file, name)
                logging.info(f"Moved document file: {name}")
    
    def unzip_folder(self, folder, name):
        if name.endswith(".zip") or name.endswith(".ZIP"):
            path = source_dir
            unpack_archive(folder, source_dir)
            move_file(dest_zip_file, folder, name)
            logging.info(f"Unzipped folder: {name}")

if __name__ == "__main__":
    # CODE FOUND AT "https://pypi.org/project/watchdog/"
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    logging.info(f'start watching directory {path!r}')
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()