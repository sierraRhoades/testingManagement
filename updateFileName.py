from datetime import datetime
import os
import argparse

def main(fileName, major_version, minor_version, verbose):
    # Get the current day of the year
    day_of_year = str(datetime.now().timetuple().tm_yday)
    while len(day_of_year) < 3:
        day_of_year = "0" + day_of_year
    year = str(datetime.now().year)[2:]
    
    version_num_str = year + day_of_year
    # new version string
    version_str = f"    #define FW_VERSION_VERSION ({version_num_str})\n"

    # regex generation for other pieces of version
    major_regex = f"    #define FW_MAJOR_VERSION (%d)\n"
    revision_regx = f"    #define FW_REVISION_VERSION (%d)\n"
    # Specify the file path
    temp_file_path = fileName + ".tmp"

    # Add default values for figuring out what versions need to be updated
    same_day = False
    rev_number = 0
    
    # Open the original file for reading and temporary file for writing
    with open(fileName, "r") as original_file, open(temp_file_path, "w") as temp_file:
        for line in original_file:
            if '#define FW_MAJOR_VERSION' in line:
                if major_version is None:
                    major_version = rev_number = int(line.split("(")[1].split(")")[0])
                else:
                    line = major_regex % major_version
            elif '#define FW_MINOR_VERSION' in line:
                if minor_version is None:
                    minor_version = rev_number = int(line.split("(")[1].split(")")[0])
                else:
                    line = major_regex % minor_version
            elif "#define FW_VERSION_VERSION" in line:
                if version_num_str in line:
                    # same date time need to flag updating the revision number
                    same_day = True
                # Modify the desired line
                line = version_str
            elif "#define FW_REVISION_VERSION" in line:
                if same_day:
                    rev_number = int(line.split("(")[1].split(")")[0])+1
                line = revision_regx % rev_number
            temp_file.write(line)

    # Replace the original file with the temporary file
    os.replace(temp_file_path, fileName)

    if verbose:
        print("Version and revision updated successfully.")

    # print version in formatted output for command parser to be able to capture the result
    print(f"{major_version}.{minor_version}.{version_num_str}.{rev_number}")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='updateVersionNum',
                        description='when called updates the version number for firmware.')
    parser.add_argument('fileName', help="name of the file to update, no relative pathing.")      # option that takes a value
    parser.add_argument("--verbose", action="store_true", 
                    help="increase details of info that this script does.")      # option that takes a value
    parser.add_argument("--majorV", default=None, type=int, help="Optional specification of major version")
    parser.add_argument("--minorV", default=None, type=int, help="Optional specification of minor version")
    args = parser.parse_args()
    var = os.getcwd()
    relative_address = args.fileName
    num_up_to_base_dir = len(var[var.find("NGRMRelaySource"):].split("\\"))
    while num_up_to_base_dir > 1:
        relative_address = "../"+relative_address
        num_up_to_base_dir = num_up_to_base_dir - 1

    if args.verbose:
        print(relative_address)   
        # print(var)
        # get_relative_addressing = os.cwd().split(")
    main(relative_address, verbose=args.verbose, major_version=args.majorV, minor_version=args.minorV)