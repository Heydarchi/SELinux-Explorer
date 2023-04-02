# SELinux-Explorer

## !! The README file needs to be updated regarding the requirements!!
<br/>

### You might need to install some packages not mentioned to run the project


<br/>
<br/>
### A utility helping developers to explorer SELinux policies. (At present it supports Android SELinux)
This project was started as a tool to use through the command line. But after some time I realized that it's crucial to have a GUI.
Having a GUI helps to provide more facilities alongside the analyzer such as filtering the result to generate custom output.
Also it leads to reusing the data rather than running the analyzer from scratch.
<br/>

### Of course, it's required some improvement in sense of architecture, performance and functionality.
<br/>
<br/>

### The supported languages are:
- file_contexts
- service_contexts
- vndservice_contexts
- hwservice_contexts
- property_contexts
- seapp_contexts
- *.te

<br/>
<br/>

The code is tested for the files mentioned above. Of course, it is not completed yet and has some flaws and issues in processing and also some refactoring to improve the performance. Very welcome to report or any kind of contribution.

Feel free to create a ticket or send me a message/report.

<br/>

### PlantUml

Generating the PNG files is based on [PlantUml](http://www.plantuml.com) that I put a jar version in this project.


## Steps to utilize the project
### 1- To run the project locally it's needed to have python 3.x and some other packages installed on your local machine
&ensp;
> Install Python 3.8 or new version, PythonIsPython3, graphviz and PyQt5
```
sudo apt install python3.8 python-is-python3 graphviz python3-pyqt5 -y
```
&ensp;

> Install dataclass-wizard and dataclasses
```
pip install dataclass-wizard dataclasses
```
&ensp;

### 2- Clone the project & the submodule
```
git clone https://github.com/Heydarchi/ClassRelExposer.git
```
Run the command below inside the cloned folder
```
git submodule update --init --recursive
```
<br/>

## **How to the GUI**
```
cd app
python main.py
```
<br/>

<br/>

### Analyzer TODO:
- [ ] Enable multi-threading
- [ ] Analyze only the changed files to save time
- [ ] Refactoring the code architecture 

### GUI TODO:
- [ ] Show the progress of analyze
- [ ] show the number of files and folder in the list
- [ ] Add a new window for search
    - [ ] Search the input file
    - [ ] Search the generated files
    - [ ] Generated output for the selected items
    - [ ] Generated output for the selected Files
- [ ] Sort result files by date
- [ ] Add AND / OR for combining the filter rules
- [ ] Making reference from path & files
- [ ] Add autocomplete for filter edit box