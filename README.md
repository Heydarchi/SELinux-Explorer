# SELinux-Explorer

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
> Install Python 3.8 or new version
```
sudo apt install python3.8
```
&ensp;
> Install PythonIsPython3
```
sudo apt-get install python-is-python3 -y
```
&ensp;
> Install graphviz
```
sudo apt-get install graphviz
```
<br/>

### 2- Clone the project & the submodule
```
git clone https://github.com/Heydarchi/ClassRelExposer.git
```
Run the command below inside the cloned folder
```
git submodule update --init --recursive
```
<br/>

## **How to run in command line**
After the packages above are installed go to the Analyzer folder and run the command below
```
cd analyzer
python FileAnalyzer.py [folder/file path]
```
<br/>

## **How to run via GUI**
```
cd analyzer
python main.py
```
<br/>

#### **To run sample** 

```
python FileAnalyzer.py ../samples
```

>The result can be found in the **out** folder




<br/>

### Analyzer TODO:
- [ ] Enable multi-threading
- [ ] Add filtering the result
- [ ] Enable using the generated data for drawing new diagrams
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
- [ ] Make it possible to open multiple diagram
- [ ] Add toolbar ( Path, File, Clear Analyze Result, Clear Result, Analyze All)
- [ ] Add lowercase/uppercase check for filter's keyword
- [ ] Sort result files by date
- [ ] Open filtered diagram automatically
- [ ] Add Folder/File to the list of search automatically
- [ ] Add AND / OR for combining the filter rules