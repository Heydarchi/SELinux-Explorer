# Contribution Guidelines

Thank you for your interest in contributing to SELinux Explorer! This document outlines the process for contributing to the project and submitting your changes.

## Setting Up Your Development Environment

1. Fork the repository on GitHub.
2. Clone your fork locally:

```
git clone https://github.com/YourUsername/SELinux-Explorer.git
```

3. Set up the required dependencies:
```
sudo ./setup.sh
```


### How to run spell check locally
There is a script to run spell check locally. It will check all the files in the `app` directory and ignore the words in the `app/config/codespell_ignore.txt` file.

```
codespell -I app/config/codespell_ignore.txt app/
```
&ensp;
### How to run spell check locally
Before pushing any changes, please run the following command to check the code style:

```
black --check app/
```
To fix the code style, run the following command:

```
black app/
```

### How to run the tests
To run the tests, run the following command:

```
pytest app/tests/
```

&ensp;

## Branch Naming Convention
Please use the patterns below to create a new branch for your changes:
&ensp;

- feature/<feature-name>: For new features or enhancements.
- bugfix/<bug-name>: For bug fixes.
- hotfix/<issue-name>: For critical fixes that need to be merged quickly.
- refactor/<component-name>: For code refactoring.
- docs/<documentation-change>: For changes in documentation.
&ensp;


## Submitting Your Changes

1. Commit your changes in your local branch.
2. Push your changes to your fork on GitHub.
3. Open a pull request against the main repository.

Please provide a clear and concise description of your changes in the pull request, including the issue or feature request it addresses, if applicable.

We will review your pull request and provide feedback or merge your changes as appropriate. Thank you for your contribution!

