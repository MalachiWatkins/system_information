# System Information Grabber
Automating the process of getting a systems specifications, to be used with an autofill application to seamlessly get system Information and insert data into a database for records and logs.

This application runs a series of commands via cmd or the terminal for Unix based operating systems (Unix Systems release TBD) to gather the system specifications
and serial numbers, once all Information has been found the application will parse the gathered data into a readable JSON format in order of the commands given. The intended use for the formatted JSON data is for a sperate app to read and auto fill into a database, I do plan on making this fully configurable but as of right now it is set up for my specific use case.

## Prerequisites
This script requires Python to be installed for it to run. There is a windows batch file as well as linux .sh file to install python (Mac TBD).

To Install Python on Windows configure the windows batch file for specific dirs if needed, then run it, CMD window will return to a default state once finished

## Usage
Once Python Is installed navigate to Get_Info folder and run sys.pyw
```
/Get_Info/sys.pyw
```
After sys.pyw is run enter the system specifications and hit confirm
if any mistakes were made while entering data hit re-do. Once Confirm is pressed a formatted JSON file is created in a folder called systeminfo in the directory that sys.pyw is in.
## Configuration
Configuration is a WIP as of now. The current Configuration is set up for my own specific use case.

DO NOT ATTEMPT TO EDIT UNLESS YOU KNOW WHAT YOU ARE DOING!!!!!
DOING SO COULD RESULT IN BREAKING THE APPLICATION AND GETTING
SCRAMBLED DATA AND AUTO FILLING DATABASES WILL WITH IT COULD RESULT IN BROKEN TABLES OR DOCUMENTS

## Contribute
If you would like to Contribute feel free to submit a pull request.
