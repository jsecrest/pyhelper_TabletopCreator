# py311-datascience-container

## Description
 Docker container template for a new project. Designed to be used directly in 
 VS code using "Reopen in container"
- python 3.11
- minimal datascience package requirements in requirements.txt
    - basic analysis, plotting, and machine learning
    - includes jupyter-notebook and jupyter-book
- ready to use with docker and the VSCode "Remote Development" extension by Microsoft
 
 ## Set up VSCode Remote Development
 1. Install Docker
 2. Install Visual Studio Code
 3. Install the Remote Development extension for VSCode

 Detailed Setup instructions for VSCode Remote Development: 
 https://code.visualstudio.com/docs/devcontainers/containers#_installation

 ## Usage
 1. From the github page of this project > "Use this template" > "Create a new repository"
 2. Clone the repository to a local directory
 3. Open the folder with VSCode. It should prompt you to "Reopen in container". 
 Click "Reopen in container" button and let the container build.
    - If the option does not pop up, try `ctrl` + `shift` + `p` to open the 
    VSCode command pallet. then search for and click 
    `Dev Containers: Reopen in Container`
    - If the vscode command pallet does not contain the above option, double
    check to make sure you correctly followed the VSCode Remote Development instructions.

