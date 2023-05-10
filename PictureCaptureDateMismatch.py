import os
import subprocess
import csv
import datetime

def get_exif_date(filename):
    """
    Function to execute the ExifTool command and retrieve the capture date from the EXIF metadata.

    Parameters:
        filename (str): Path to the file.

    Returns:
        str or None: Capture date in the format '%Y%m%d' or None if an error occurred.
    """

    result = subprocess.run(['exiftool', '-CreateDate', '-d', '%Y%m%d', '-s3', filename], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None

def get_file_date(filename, mask, date_format):
    """
    Function to analyze the file name and retrieve the date according to the specified mask and format.

    Parameters:
        filename (str): File name.
        mask (tuple): Date mask in the format (start_index, length).
        date_format (str): Expected date format.

    Returns:
        str or None: Date from the file name in the format '%Y%m%d' or None if the date format is incorrect or the date is before 1900.
    """

    try:
        basename = os.path.basename(filename)
        date_str = basename[mask[0]:mask[0] + mask[1]]  # Retrieve the portion of the file name according to the mask
        date_str = date_str.replace('_', '-').replace('-', '')  # Remove '_' and '-' characters

        # Check if the date format is correct
        parsed_date = datetime.datetime.strptime(date_str, date_format)
        parsed_date_year = parsed_date.year

        # Check if the date is after 1970
        if parsed_date_year < 1900:
            return None

        return parsed_date.strftime('%Y%m%d')
    except (ValueError, TypeError):
        return None


def main():
    """
    Main function of the program.
    """

    # Define the file name mask and date format
    mask = (0, 8)  # Sample mask - starts at index 0 and has a length of 8 characters
    date_format = "%Y%m%d"  # Sample date format

    # Create the CSV file
    csv_file = open('output.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['File Name', 'Location', 'File Date', 'EXIF Capture Date'])

    # Traverse all files in the folder and subfolders
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith('.jpg'):
                filename = os.path.join(root, file)
                file_date = get_file_date(filename, mask, date_format)
                exif_date = get_exif_date(filename)
                if file_date and exif_date and file_date != exif_date:
                    csv_writer.writerow([file, filename, file_date, exif_date])

    # Close the CSV file
    csv_file.close()
    print("Program finished. Results have been saved to output.csv.")

if __name__ == "__main__":
    main()
