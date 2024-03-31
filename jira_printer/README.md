# For Developers
Hi, I hope you find my project exiting :)

## Info
Used IDE: Pycharm Community Edition

## Import are pain
As you can see, I have two `__main__.py` files. There are reasons for it.

### python -m jira-printer
I wanted to use this beautiful command line command to be used to start the program. Problems?
Project structure. As you can see, the actual code is situated in sub-folder. 
In order for that to run, there must be a `__main__.py`. So I created this one. 
As I was using this command I was forced [by Pycharm] to use relative imports (`from .sth import anyth`)

### PyInstaller
The main cool thing about this project is that it is not meant for developers.
It is mainly focused on the people working with Jira: Scrum Masters, Team Coaches and Project Leads.
As I cannot assume that my audience has coding experience, I wanted to create a standalone file for my project.
This way a person not familiar with python, its dependencies and installing a python program can still use my app.
Because I want to encourage this for my fellow developers, who may be modifying this program, I have included a spec file for `PyInstaller` (`jira-printer.spec`). 
As I myself have experienced the pain of docs of `PyInstaller`, I did not want for others to suffer more.

For the sake of simplicity, I have placed a `jira-printer.spec` file in the parent folder.

As you may remember from the previous section, I have used relative imports. And yes, it is a problem in s single-file program.
This way my relative imports were an import error as there is no parent folder. So I had to give an access point for my program one level above its actual place.
Here comes the second `__main__.py` above the first one. It is the only way to solve the relative import problem.

### Project Structure
I did not want to pack all the python files in main folder. So I had my pain with executing evening I wanted "out of the box".
All the same who uses it. If you have any better ideas than me (and it is still that simple), please tell me. I love to learn!

# For others, who do not work on this project but may be struggling with PyInstaller
If you have the same situation as me: you try to build your project with PyInstaller in subpackage,
you create an access point one package, and you still cannot import your subpackage:
**delete an** `__init__.py` **from your parent package!** It could be, that I am not this experienced in such python projects,
but it took me several hours on my weekend. Do not do my errors! I hope google and co. will parse this page.

For them my history searches:
* pyinstaller importerror cannot import name from
* pyinstaller importerror cannot import name
* pyinstaller attributeerror module has no attribute
* pyinstaller no module named

The documentation for PyInstaller specs has come for me too short. The most answers were due to hiddenimport, which I have also tried, however without success.
I hope, that this README can help others struggling with problem.

