
# SELinux Explorer
<br/>

SELinux Explorer is a utility designed to help developers explore SELinux policies, with a focus on Android SELinux at present. The project initially started as a command-line tool but has since evolved to include a graphical user interface (GUI) for better usability and to provide additional features such as filtering, generating custom output, and reusing data.

The tool supports the following file types:
- `file_contexts`
- `service_contexts`
- `vndservice_contexts`
- `hwservice_contexts`
- `property_contexts`
- `seapp_contexts`
- `*.te`

**Please note**: The tool is a work in progress and might have some issues or require performance improvements. We welcome any bug reports, suggestions, or contributions.

<br/>

### Screenshots of the GUI and the generated output
#### GUI
![GUI](./screenshots/gui.png)
<br/>
#### Outputs
![GUI](./screenshots/top_view_1.png)
<br/>
![GUI](./screenshots/sequential_1.png)

<br/>

## Dependencies

To run SELinux Explorer, you need to have Python 3.x and some other packages installed on your local machine:

- Python 3.8 or newer
- PythonIsPython3
- Graphviz
- PyQt5
- Dataclass-wizard
- Dataclasses

## Installation
#### Note : The 1st & 2nd steps can be skipped by runnig the `setup.sh` script.
```
./setup.sh
```
&ensp;

1. Install Python 3.8 or a newer version, PythonIsPython3, Graphviz, and PyQt5:

```
sudo apt install python3.8 python-is-python3 graphviz python3-pyqt5 -y
```
&ensp;


2. Install python packages

```
pip install -r requirements.txt
```

&ensp;

3. Clone the project and its submodule:

```
git clone https://github.com/Heydarchi/SELinux-Explorer.git
```
&ensp;

4. Inside the cloned folder, run the following command to update the submodule:

```
git submodule update --init --recursive
```
<br/>

## How to Run the GUI

1. Change to the `app` directory:

```
cd app
```

2. Run the main.py script:

```
python main.py
```
<br/>

## Contributing

Thank you for your interest in contributing to SELinux Explorer! We welcome and appreciate any contributions, whether it's bug reports, feature requests, code, documentation, or testing. Please refer to our [CONTRIBUTION.md](CONTRIBUTION.md) file for detailed guidelines on how to set up your development environment, check code style, run tests, and submit your changes.

## Features and TODOs

This project is under active development, and we're continuously working on improving and expanding its functionality. For a detailed list of features and tasks that we're planning to implement, please refer to the [TODO List](TODO.md) file. We welcome your contributions and feedback, so feel free

## Bug Reports:

If you encounter any issues or bugs while using SELinux Explorer, we encourage you to report them so we can address and fix them promptly. Please create a new issue using our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) and provide all the necessary details to help us reproduce and understand the problem. Your feedback is invaluable in helping us maintain the tool's reliability and stability.

## Feature Requests:

We're always looking to improve and expand the functionality of SELinux Explorer. If you have a suggestion for a new feature or an enhancement to an existing one, we'd love to hear from you. Please create a new issue using our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md) and provide a clear and concise description of your idea, including the problem it aims to solve and the benefits it would bring. Your input is essential in shaping the future development and direction of the project.

## License

This project is released under the [MIT License](LICENSE).

