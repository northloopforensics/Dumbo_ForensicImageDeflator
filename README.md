DUMBO: Deflate Unnecessary Megabytes By Overwriting

A script to ID files based on MD5 hash and reduce the file to zero bytes if the hash exists in a provided list. 

This will leave the folder and file structure unchanged.

The intended application was to aid in reducing the size of digital forensic training data sets while providing the appearance of a complete system.  

It can also be used to redact file data for case work related to ICAC or similar issues where file representation and nonproliferation are required.

To run:

1. Assign paths for the variables report_file - text report showing truncated files, hash_file - an MD5 hash list with one hash per line, and image_name - the directory containing the files to be reviewed.
2. If working with an image file (E01, .bin, .001) mount the image and allow cached changes.
3. Run the script on the root of the mounted image.
4. Re-image your mounted directory structure.

The Releases section of this repo has a sample MD5 hash set created from the NIST NSRL hash set.  
