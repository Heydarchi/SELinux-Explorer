# SELinux-Explorer
A utility helping developers to explorer SELinux policies


### The supported languages are:
- file_contexts
- service_contexts
- vndservice_contexts
- hwservice_contexts
- property_contexts
- seapp_contexts
- *.te

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

## **How to run**
After the packages above are installed go to the Analyzer folder and run the command below
```
cd analyzer
python FileAnalyzer.py [folder/file path]
```
#### **To run sample** 

```
python FileAnalyzer.py ../samples
```

>The result can be found in the **out** folder

<br/>

### TODO:
- [ ] Fix extracting rules for multiple source/target/etc in one line
- [ ] Enable multi-threading
- [ ] Add filtering the result
- [ ] Enable using the generated data for drawing new diagrams
- [ ] Analyze only the changed files to save time
- [ ] Refactoring the code architecture 