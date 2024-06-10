from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = ""
dest_music_dir = ""
dest_image_dir = ""
dest_document_dir = ""
dest_video_dir = ""

music_file_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.alac', '.aiff', '.aif', '.aifc', '.opus', '.mp2', '.mka', '.mid', '.midi', '.rmi']
image_file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico', '.heic', '.heif', '.raw', '.cr2', '.nef', '.orf', '.sr2', '.psd', '.ai', '.eps']
video_file_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2', '.ogv', '.rm', '.rmvb', '.vob', '.ts', '.m2ts', '.mxf', '.divx']
document_file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']

#TODO: Create a function of each file type downloaded
#TODO: Create constant function: if __name__ == "__main__":...

def move_file(destination, file, name):
    filename, extension= splitext(name)
    # if exists(destination):
    #    pass
    move(file, destination)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for e in entries: # GO THROUGH EACH FILE
                name = e.name
                self.move_music_file(e, name)
                self.move_image_file(e, name)
                self.move_video_file(e, name)
                self.move_doc_file(e, name)
    
    def move_music_file(self, file, name):
        for e in music_file_extensions:
            if file.endswith(e) or file.endswith(e.upper()):
                move_file(dest_music_dir, file, name)
                logging.info(f"Moved music file: {name}")
    
    def move_image_file(self, file, name):
        for e in image_file_extensions:
            if file.endswith(e) or file.endswith(e.upper()):
                move_file(dest_image_dir, file, name)
                logging.info(f"Moved image file: {name}")
    
    def move_video_file(self, file, name):
        for e in video_file_extensions:
            if file.endswith(e) or file.endswith(e.upper()):
                move_file(dest_video_dir, file, name)
                logging.info(f"Moved video file: {name}")
    
    def move_doc_file(self, file, name):
        for e in document_file_extensions:
            if file.endswith(e) or file.endswith(e.upper()):
                move_file(dest_document_dir, file, name)
                logging.info(f"Moved document file: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = MoveHandler()