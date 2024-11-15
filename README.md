# TreeDoc
I wrote this simple Python program to help me with school work. Instead of copy pasteing the output of `tree` I wanted to have a tool that would make it much more attractive to have your file structure attached to your documentation. 

## Install:
1. git clone intwo any directory you like.
2. execute the setup script with ./setup.sh from the directory you installed to (give it permissions with chmod u+x setup.sh if need be). This script will add the current directory to your PATH. If you do not want the program to be installed in this way, do it manually instead. 
3. source ~/.bashrc in your console to enable PATH.
4. The Script can now be used anywhere on your system and it will save the file to the folder you specify/ use it in. 

## Usage: 
call 'td' anywhere you like. 
the porgram takes two arguments: 

positional argument path is standard '.', can be changed. 

-d or --depth takes an int and specifies how deep into the given directory the program should go. Default is 9999.

## examples: 

This will make a file tree of your current directories and all it's sudirectories. 
```bash
td
```

```bash
td path/to/project
```

```bash
td /etc -d 1
```