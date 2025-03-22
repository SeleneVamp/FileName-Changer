# Switch from os and fmatch libaray to pathlib for modern way. I.e this is for using .stem eaither than it would be on os
from pathlib import Path

def main():

    # Get Folder Path
    FolderPath = input(r"Enter Folder Path: ") + "\\"

    # Sets number of changes to be made to file names + Sets the variable as an Int
    NumChanges = input("How many changes you wish to do: ")
    NumChanges = int(NumChanges)

    # Creates empty arrays
    BeforeValues = []
    AfterValues = []

    # Loops through asking for what is to be changed in the file name,
    for i in range(NumChanges):
        i = i + 1
        BeforeValues.append(input("Change %i from: " % i))
        AfterValues.append(input("Change %i to: " % i))

    # Loops through the Files and changes the names to match the changes requested
    for File in Path(FolderPath).iterdir():
        if not File.is_file():
            continue

        FileName = File.stem
        for Before, After, _ in zip(BeforeValues, AfterValues, range(NumChanges)):
            FileName = FileName.replace(Before, After)
        FileName = FileName + File.suffix
        print(File.parent)
        File.rename(File.parent/FileName)


main()
