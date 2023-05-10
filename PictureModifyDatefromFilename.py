import subprocess
import csv

def modify_exif_dates(csv_file):
    """
    Function to modify the EXIF capture dates based on the values in the third column of the CSV file.

    Parameters:
        csv_file (str): Path to the CSV file.

    Returns:
        None
    """

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row

        modified_files = []  # Store the modified file names

        for row in csv_reader:
            file_name = row[0]
            exif_date = row[2]

            # Modify the EXIF capture date of the image
            result = subprocess.run(['exiftool', '-CreateDate=' + exif_date, file_name], capture_output=True, text=True)
            if result.returncode == 0:
                modified_files.append(file_name)

        if modified_files:
            print("Modified EXIF dates for the following files:")
            for file_name in modified_files:
                print(file_name)
        else:
            print("No EXIF dates modified.")

def main():
    """
    Main function of the program.
    """

    csv_file = 'output.csv'  # Path to the generated CSV file

    modify_exif_dates(csv_file)

if __name__ == "__main__":
    main()
