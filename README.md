# Jira Printer

A small program to print beautiful Jira tickets.

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
<img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&amp;logo=Jira&amp;logoColor=white"/>

## Description

This project was inspired by searching for printing possibilities of Jira tickets for PI Planning.
At the time being, Jira plugins that produce beautiful Jira cards are very expensive and those plugins that are free are not that appealing, so I have come to an idea to create my own program for these needs.
Jira Cards is a straight forward program that processes a .csv full export file from Jira into some beautiful cards ready to be printed and tossed across that PI Planning board!

## Getting Started

### Dependencies

* Python

### Installing

* Ready to download .exe files can be found in releases
* Source code is available in the current repo
* For those who want to modificate the program and be able to create a single file runnable, there is a .spec file for pyinstaller.

### Executing program

* install requirements
* run
```
python -m jira_printer
```

### Creating a one-file .exe

* install requirements
* install pyinstaller 6.5.0
* run
```
pyinstaller jira-printer.spec
```

## Help

If you need any help with a program, open a new discussion.

## Authors

Anna Tsarenko

## License

This project is licensed under the GPL 3.0 License - see the LICENSE.md file for details.