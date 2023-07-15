# Mass FileName Changer
This is a program that will rename all the files in a directory

If you had a nummber of files that all had in some text in the name that you didn't want or you just downloaded files/ a torrent and you want it to fit into a naming format of your liking. Then this program will loop through each file and rename it to the pararmeters that you give it.

I orginally created it so i could rename around 10+ torrent files quicker than i could it i went 1 by 1.

For example say you have a torrent files with the same name as **Marvels.Iron.Fist.S01E01.2160p.10bit.NF.WEBRip.5.1.x265.HEVC-MZABI** with only the episode number changing throughout the file names. so you'll want to get rid of everything after "E01" and all the fullstops, and say you want to add something into the name you can.


So we have;
- **Marvels.Iron.Fist.S01E01.2160p.10bit.NF.WEBRip.5.1.x265.HEVC-MZABI.mkv**

And we want to make it;
- **Marvels Iron Fist - S01E01.mkv**

## Running the Program
So after either opening the program in a python runner or using the .bat file, the first thing we'll want to do is give it the file location of the files that we're wanting to rename.

![image](https://github.com/SeleneVamp/Mass-File-Name-Changer/assets/139238196/216257c4-171f-4d19-96fb-e52e5542f81c)

After that it will ask how many changes we want to make to the file names. So in this case its 4 changes;

- 1, Removing ".2160p.10bit.NF.WEBRip.5.1.x265.HEVC-MZABI"/n
- 2, Removing "."
- 3, Add a "." back to infront of the file extenstion
- 4, Add " - " between Fist and S01

![image](https://github.com/SeleneVamp/Mass-File-Name-Changer/assets/139238196/829e42df-2e1f-41cf-833d-52bf8397c3cc)

After entering how many changes we want to do, it will go through each of the changes asking use what it currently is and then what we want it to become.

![image](https://github.com/SeleneVamp/Mass-File-Name-Changer/assets/139238196/e9ed11a8-cf7e-40bd-91ac-86a21dad6b87)

As you can see above I've gone through and entered what it is i want changing and what i want it changing to. 
- For the first one i entered everything after "E0" and the change to is left blank as we want to get rid of it completely.
- The second one entered a fullstop "." as wanting to be changed and change to is a space (just one space)
- For the thrid one as all the "." have been removed that includes the one between the file name and the file name extention so that needs putting back. So its changed from a space (just one space as thats what we replaced "." with) then the file name extention E.g **" mkv"** and its changed to **".mkv"**
- And lastly we wanted to add a bit of formating so we changed from **"Fist S01"** (as thats that it will look like by the time this change is made) and change it to **"Fist - S01"**

![image](https://github.com/SeleneVamp/Mass-File-Name-Changer/assets/139238196/08dec0f3-97e6-4511-a214-1fd17ef937e0)

As you can see it will go through each change you enter and make them to the files in the directory that you gave it at the beginning, After that it will start over again.

## Thing's to rememeber

- When entering the Files directory it only need to go to the folder that holders the files, its not the directory of each file its self. You also don't need to add an ending "\" as the program does that for you. So For example
  - **X:\Shows\Marvels Iron Fist\Season 01** (Correct Format)
  - **X:\Shows\Marvels Iron Fist\Season 01\Iron Fist S01E01.mkv** (Wrong Format)

- If you entered the wrong number for the amount of changes or if you realise that you need more or less then thats not an issue.
  - You can either close the program as no changes are made till you enter the last change you want making
  - You can continue and when it looks back around make the changes that still remain after having done the ones you could enter
  - If you don't need as many as you entered, you entered 4 but only need 2 then when you come to the 3rd and 4th changes if you leave them blank know change will done for them, as its not able to match to anything to change.

- When entering the changes that your wanting you need to keep in mind that  each change is done one after the other so you need to take that into account when saying what it is thats being changed For exampple
  - When adding the **" - "** to between the show name and show season + episode numbers, when it gets to making this change it won't look like this: **Marvels.Iron.Fist.S01E01.2160p.10bit.NF.WEBRip.5.1.x265.HEVC-MZABI.mkv**
  - It will look like this: **Marvels Iron Fist S01E01.mkv**
  - So you need to take into account what it is your channging from otherwise it wont work

- Should you enter the wrong change from or change to you will need to restart the program as editing the changes as yet to be implemented into the program

## Files Included

- FileName Changer.py
  - This is the python file that contains the code for the program
- FileName Changer.bat
  - This is a bat file that runs the python file, if you don't want to have to open the python file every time you want to run this program
  - The bat file doesn't need to be in the same location as the python file as long as it links to it (i.e. Shortcut)

## Future Improvements

In the future i would like to add these things to the program just to make it a bit more user friendly and nicer. While i know there is probably programs out there that already do what this program does, it wasn't made by me.

- Create a GUI rather than having to run it from a python runner or a bat file
-  Add the ablility to change the users file name changes before the program run with it. (This can probably be done with the GUI as it will have text boxes that get filled in and wont take the info till the run button is clicked)
-  Add more or less changes while doing the changes rather than being stuck to a set number and haing to repeat the process again or having to restart the program.
-  Have it ignore the filename extention so users don't have to worry about having that being apart of the file name change
