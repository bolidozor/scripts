<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>scripts
</h1>
<h3>◦ Unleashing Power, Script by Script!</h3>
<h3>◦ Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Markdown-000000.svg?style&logo=Markdown&logoColor=white" alt="Markdown" />
</p>
<img src="https://img.shields.io/github/languages/top/bolidozor/scripts?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/bolidozor/scripts?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/bolidozor/scripts?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/bolidozor/scripts?style&color=5D6D7E" alt="GitHub license" />
</div>

---

##  Table of Contents
- [ Table of Contents](#-table-of-contents)
- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#project-structure)
- [ Modules](#modules)
- [ Getting Started](#-getting-started)
- [ Roadmap](#-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---


##  Overview

The scripts repository within Bolidozor is composed of Python scripts useful to station administration. It features functionalities like executing coordinated commands on multiple remote radio stations, detecting linearly frequency-modulated signals, and analyzing data files. With precise value filtration, optimized data extraction, visualization, and remote station coordination.

---

##  Features

| **Feature**                | **Description**                                                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| ** Architecture**                         | Modular architecture centered around script-based implementations, with diverse utilities for signal detection, file parsing, and remote executions. |
| ** Documentation**                   | Documentation is minimalistic and could be improved to explain the purpose/usage of all scripts/features for enhanced understandability.                      |
| ** Dependencies**                      | The project relies on common Python libraries like NumPy for mathematical operations and Paramiko for remote SSH connectivity.                             |
| ** Modularity**                        | Scripts are neatly structured for handling specific tasks, showing good modularity which aids in maintainability and flexibility of the codebase.                   |

---


##  Project Structure




---

##  Modules

<details closed><summary>Root</summary>

| File                                                                                | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---                                                                                 | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [extract.py](https://github.com/bolidozor/scripts/blob/main/extract.py)             | The script reads file(s) passed as arguments and extracts date and time from each line. Then it subtracts 5 minutes from each datetime object. These manipulated dates and times are stored and converted to a correct format for future use in terminal commands. Lastly, it issues a terminal command to list the contents of a certain directory on a remote server through SSH.                                                                                                                                |
| [lfms_detector.py](https://github.com/bolidozor/scripts/blob/main/lfms_detector.py) | The Python script is a signal processing application that detects linearly frequency-modulated signal segments. The script splits signal samples into frames, multiplies the frames by a window function and processes them through Discrete Fourier Transform (DFT). The script then generates a 2D array and searches for the local maxima of each frame. The identified maxima signify the detection of frequency-modulated signals. The script also produces waterfall plots of the detections.                |
| [bzfind](https://github.com/bolidozor/scripts/blob/main/bzfind)                     | The script utilizes python to parse specific file formats through Bolidozor's file software structure. It searches for files in the predefined repository root, and extends the functionality for sorting data files with unique operations; such as limiting time of origin, collection path, and filename with regex filters. Upon successful matching guided by user-defined parameters, it yields the found entities as output. It’s especially useful for dealing with bulk recordings and snapshot handling. |
| [bzremote](https://github.com/bolidozor/scripts/blob/main/bzremote)                 | This Python script, bzremote, executes pre-specified commands on multiple remote Bolidozor radio monitoring stations concurrently. A hostname list from a designated file determines the commands' target hosts. You can specify the commands using templates, replacing a placeholder, "%" with the hostname. Additionally, adjustable options include changing the default host-group set and varying the count of concurrently running command instances.                                                       |

</details>

---

##  Getting Started

###  Installation

1. Clone the scripts repository:
```sh
git clone https://github.com/bolidozor/scripts.git
```

2. Change to the project directory:
```sh
cd scripts
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

###  Using scripts



#### bzremote
The ./bzremote sshpass -p odroid ssh % df -h should not be used anymore. The stations should be accessed using a private key (shared for selected users at space.astro.cz). Then the bzremote script can be run without sshpass, e.g. ./bzremote ssh % df -h


##  Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## License

This project is licensed under the GPL 3 License. 


