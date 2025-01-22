#   PYTHON 3
#   NIST BASED IMAGE SET CLEANER
#
#   A tool to truncate forensic image set for training purposes using MD5 hash list.

#   TO DO 
#   -   Add a report of changed files - full path and data savings - DONE
#   -   Get a clean NSRL hash list - DONE

import os
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

########### GLOBAL VARIABLES #####################

report_file = 'path_to_report.txt'
hash_file = 'path_to_hash_list.txt'
image_name = 'path_to_image directory'
now = datetime.now()
nsrl_list = set()
byte_counts = []


#******************* Functions *****************************

def compute_md5(filename):
    hash_md5 = hashlib.md5()
    try:
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return filename, hash_md5.hexdigest()
    except Exception as Problem:
        print('Problem with ', filename, ' - ', Problem)
        return filename, None

def process_file(filename):
    try:
        filename, file_hash = compute_md5(filename)
        if file_hash and file_hash in nsrl_list:
            file_size = os.path.getsize(filename)
            print('TRUNCATED - ', filename, ' - Removed ', file_size, ' Bytes')
            with open(filename, 'w') as inputfile:
                byte_counts.append(file_size)
                inputfile.truncate(0)
            with open(report_file, 'a') as report:
                report.write(filename)
                report.write('\n')
    except PermissionError:
        print('Permission denied for - ', filename)
    except OSError:
        print('Access error for - ', filename)
    except FileNotFoundError:
        print('File not found for - ', filename)

def md5_truncate():
    with open(report_file, 'w') as report:
        report.write("DUMB0 REPORT \n")
        report.write("Target Volume/Folder - ")
        report.write(image_name)
        report.write('\n')
        report.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        report.write('\n\n')
        report.write('Files Reduced to 0 Bytes: \n\n')

    with open(hash_file, 'r') as f:
        print("Caching hash list.....") #read hash list to a set for faster lookup
        for line in f:
            line = line.strip().lower()
            nsrl_list.add(line)

    with ThreadPoolExecutor() as executor:      #process files concurrently
        for root, subfolder, files in os.walk(image_name):
            for items in files:
                filename = os.path.join(root, items)
                executor.submit(process_file, filename)

    total_bytes = sum(byte_counts)
    gigabytes = total_bytes / 1073741824
    with open(report_file, 'a') as report:
        report.write('\n\n\n')
        report.write("Total Bytes Removed - ")
        report.write(str(gigabytes))
        report.write(' GB')
    print('Total Bytes Removed - ', gigabytes, ' GB')
md5_truncate()
