from datetime import datetime
import os
import piexif

directory = 'images'
for entry in os.scandir(directory):
    if entry.is_file():
        if entry.name.startswith('IMG_'):
            exif_dict = piexif.load(entry.path)
            data = entry.name.rstrip('.jpg').split('_')
            date = data[1]
            year, month, day = map(int, (date[0:4], date[4:6], date[6:8]))
            time = data[2]
            hour, minute, second = map(int, (time[0:2], time[2:4], time[4:6]))
            new_date = datetime(year, month, day, hour, minute, second).strftime("%Y:%m:%d %H:%M:%S")
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
            exif_bytes = piexif.dump(exif_dict)
            piexif.remove(entry.path)
            piexif.insert(exif_bytes, entry.path)
