# CBAS-full
Using Particle mesh devices for environmental sensor streaming and Plotly/Dash for visualization

## Environment Setup  

#### Resources

* [Conda Cheet Sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)

* [Miniconda Docs](https://docs.conda.io/en/latest/miniconda.html)

* [Tmux Cheat Sheet](https://tmuxcheatsheet.com/)

* [TMUX guide](https://tmuxguide.readthedocs.io/en/latest/index.html)

---

We need to setup an isolated Python environment where the necessary libraries will be installed. 
You can use either Anaconda or Pyenv for this, depending on the situation.

  1. Install:
     * Python 3+
     * Condas or virtual env
  2. Python libraries  
     * If using conda, it is advised to install using condas first, then pip for the `PyparticleIO` library.
  
---  
## Miniconda Setup

### Download and install Miniconda

1. Download latest version of Miniconda here:  
https://docs.conda.io/en/latest/miniconda.html

* From here, its best to follow instructions as per your OS

---
  * On linux
  
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    ```

* Then run the installation script:

    ```bash
    bash Miniconda3-latest-Linux-x86_64.sh
    ```

---

2. Run through promts in set-up and once installed,Restart terminal to finish.
  

3. If you'd prefer that conda's base environment not be activated on startup: 
  (conda does not activate everytime you start your terminal) 
  
  ```bash
    conda config --set auto_activate_base false
  ```

## Creating conda environments

Once conda is installed and initialized, (You can do something like `conda activate` in the terminal) we want to create a new environment within our CBAS-full directory.

* [Docs.conda.io - Specifying a location for an environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment)

There are multiple ways to create our conda environment:

1. [Using environment.yml file](#environment-file)
2. Manual installation
3. using spec-file.txt (Platform specific)

---

### environment-file
  
1. Navigate to CBAS-full directory 

2. Using evironment.yml
  ```bash
  conda create -f environment.yml
  ```
3. Then install one more library:

* Instal PyparticelIO
  
  ```bash
  pip install pyparticleio
  ```

---

Or

### Manual-install

* We can install manually:
  
Somewhat manual install...

```bash
conda create ---prefix ./env
```

To activate the environment:

```bash
conda activate ./env
```

Then install one more library:

* Instal PyparticelIO
  
  ```bash
  pip install pyparticleio
  ```

 ---

## Pyenv Setup 

#### pip installation

* setup virtual environment 
  * Create environment from the requirements.txt file:
  
    ```bash
    
    ```
  
#### TMUX shared libraries


## VM Environment Setup  

For setting up required software/libraries to run code on a virtual machine.
Tested on Gcloud Debian GNU/Linux, 10 (buster) image.

## Resources

* [Conda Cheet Sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)

* [Miniconda Docs](https://docs.conda.io/en/latest/miniconda.html)

* [Tmux Cheat Sheet](https://tmuxcheatsheet.com/)

* [TMUX guide](https://tmuxguide.readthedocs.io/en/latest/index.html)

---

#### On initial boot

* Update system

```bash
sudo apt-get update&&sudo apt-get upgrade
```

* Install wget

```bash
sudo apt-get install wget
```

* Install Git

```bash
sudo apt-get install git
```

* Clone CBAS-Full Git Repository

```bash
git clone https://github.com/phzx3691/CBAS-full.git
```

## Usage

* Create `config.py`:
  
  In folders where script is running, a `config.py` is needed

  ```bash
  nano config.py
  ```

    Where you need the following variables:

    ```

    Particle_key = "XXXXXXXXXXXXXXXXXXX"
    user = "[USER]"
    passwd = "[PASSWORD]"
    host = XXX.XXX.XXX
    ```