import os
import fnmatch

def main():

    # Get Folder Path
    FolderEnd = "\\"
    FolderPath = input(r"Enter Folder Path: ")
    FolderPath = FolderPath + FolderEnd

    # Getting files in folder for renaming
    FileForRename = fnmatch.filter(os.listdir(FolderPath), '*')

    # Creates empty arrays
    BeforeValues = []
    AfterValues = []

    # Sets number of changes to be made to file names + Sets the variable as an Int
    NoChanges = input("How many changes you wish to do: ")
    NoChanges = int(NoChanges)

    # Loops through asking for what is to be changed in the file name, for the number of changes set before and adding them
    # to the arrays created before
    for i in range(NoChanges):
        i = i + 1
        BeforeValues.append(input("Change %i from: " % i))
        AfterValues.append(input("Change %i to: " % i))

    # Loops through the NoChanges for each file
    for o in range(NoChanges):
        print(o)
        for FileName in FileForRename:
            os.rename(FolderPath + FileName, FolderPath + FileName.replace(BeforeValues[o], AfterValues[o]))
        FileForRename = fnmatch.filter(os.listdir(FolderPath), '*')
        o += 1

    main()

main()

