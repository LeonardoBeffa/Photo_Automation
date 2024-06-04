from exif import Image
from os import scandir, rename, makedirs
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#diretorios.
source_dir = "H:\\Documentos\\Backup do PC\\Imagens\\iPhone - Galaxy"
dest_dir_DontExif = f"{source_dir}\\DontEXIF"
dest_dir_video = f"{source_dir}\\videos"
year_dirs = {year: f"{source_dir}\\{year}" for year in range(2010, 2025)}

#image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jfif", ".jif", ".jfi", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def ensure_directory_exists(directory):
    if not exists(directory):
        makedirs(directory)

def move_file(dest, entry, name):
    ensure_directory_exists(dest)
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

def inf_photo(name,photo):
    if photo.has_exif:
        print("----------------------------")
        print(f"{name}")
        print("----------------------------")
        print(f"Device information")
        
        try:
            print(f"Make: {photo.make}")
            print(f"Model: {photo.model}")
        except AttributeError:
            print("NAO TEM MAKE & MODEL")

        print("----------------------------")
        print(f"GPS Location.")
        
        try:
            def format_dms_coordinates(coordinates):
                return f"{coordinates[0]}° {coordinates[1]}\' {coordinates[2]}\""

            def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
                decimal_degrees = coordinates[0] + \
                                coordinates[1] / 60 + \
                                coordinates[2] / 3600
                
                if coordinates_ref == "S" or coordinates_ref == "W":
                    decimal_degrees = -decimal_degrees
                
                return decimal_degrees
            
            print(f"Latitude (DMS): {format_dms_coordinates(photo.gps_latitude)} {photo.gps_latitude_ref}")
            print(f"Longitude (DMS): {format_dms_coordinates(photo.gps_longitude)} {photo.gps_longitude_ref}\n")
            print(f"Latitude (DD): {dms_coordinates_to_dd_coordinates(photo.gps_latitude, photo.gps_latitude_ref)}")
            print(f"Longitude (DD): {dms_coordinates_to_dd_coordinates(photo.gps_longitude, photo.gps_longitude_ref)}\n")
        
        except AttributeError:
            print("NAO TEM GPS.")

        print("----------------------------")
        print(f"Date & time")
        print(f"{photo.datetime_original}\n")
    else:
        print("-------------------------")
        print(f"{name}")
        print("EXIF 0.")
        print("-------------------------")

class MoverHandler(FileSystemEventHandler):
     def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_image_files(entry, name)
                self.check_video_files(entry, name)
    
     def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name} - Para a pasta: Video")

     def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                with open(source_dir + "\\" + name, "rb") as file_photo:
                    
                    photo = Image(file_photo)

                    if photo.has_exif:
                        
                        try:
                        
                            date = photo.get("datetime_original")
                            if date == None:
                                file_photo.close()
                                move_file(dest_dir_DontExif, entry, name)
                                logging.info(f"Moved image file: {name} - Para a pasta: DontExif")
                            else:
                                for year in range(2010, 2025):
                                    if str(year) in date:
                                        file_photo.close()
                                        move_file(year_dirs[year], entry, name)
                                        logging.info(f"Moved image file: {name} - Para a pasta: {year}")
    
                        except AttributeError:
                            continue                                                                                        

                    else:   
                        file_photo.close()
                        move_file(dest_dir_DontExif, entry, name)
                        logging.info(f"Moved image file: {name} - Para a pasta: DontExif")               

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()