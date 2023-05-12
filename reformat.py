import os
import time
import jdatetime
from tqdm import tqdm
from glob import glob
from datetime import datetime

data_dir = r'data\**\*.*'
new_dir = r'data\new'
image_video_extension = ['jpg', 'mov', 'mp4', 'mkv', 'png', 'heic', 'jpeg', 'gif', 'webp', 'm4v']
format_data = "%a %b %d %H:%M:%S %Y"

persian_month = {
    1: '01-فروردین',
    2: '02-اردیبهشت',
    3: '03-خرداد',
    4: '04-تیر',
    5: '05-مرداد',
    6: '06-شهریور',
    7: '07-مهر',
    8: '08-آبان',
    9: '09-آذر',
    10: '10-دی',
    11: '11-بهمن',
    12: '12-اسفند'
}
data_list = glob(data_dir, recursive=True)
count = 0
not_moved = []
for file in tqdm(data_list):
    file_type = str(file.split('.')[-1]).lower()
    if file_type in image_video_extension:
        time_modified = os.path.getmtime(file)
        time_data = time.ctime(time_modified)
        date = datetime.strptime(time_data, format_data)
        persian_time = jdatetime.date.fromgregorian(day=date.day, year=date.year, month=date.month)
        path = f'{new_dir}/{persian_time.year}/{persian_month[int(persian_time.month)]}'
        os.makedirs(path, exist_ok=True)
        new_file_name = f'{path}/{persian_time.year}{str(persian_time.month).zfill(2)}{str(persian_time.day).zfill(2)}'
        count = len(glob(f'{new_file_name}*.*'))
        os.rename(file, f'{new_file_name}_{str(count + 1).zfill(4)}.{file_type}')
        count += 1
    else:
        not_moved.append(file_type)

print(f'{count} of {len(data_list)} file has moved...')
print(f'{len(data_list) - count} can not moved...')

print(set(not_moved))
