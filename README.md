# CBAS-full
Using Particle mesh devices for environmental sensor streaming and Plotly/Dash for visualization

## Environment Setup  

  1. Install:
     * Python 3+
     * Condas or virtual env
  2. Python libraries  
     * If using conda, it is advised to install using condas first, pip at a last resort.
  
#### Conda installation

* [Docs.conda.io - Specifying a location for an environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment)
* Create environment from the environment.yml file:
  
  ```bash
  conda create -f environment.yml
  ```

* Instal PyparticelIO
  
  ```bash
  pip install pyparticleio
  ```

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

---

#### Download and install Miniconda

* Download latest version of Miniconda here:  
https://docs.conda.io/en/latest/miniconda.html

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

* Then run the installation script:

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

* Run through set-up and Condas should be installed, restart terminal to finish install

* If you'd prefer that conda's base environment not be activated on startup:  

```bash
conda config --set auto_activate_base false
```

## Usage

* Create `config.py`:
  
  ```bash
  nano config.py
  ```

    Where you need the following variables:

    ```

    Particle_key = "XXXXXXXXXXXXXXXXXXX"
    user = "XXXX"
    passwd = "XXXXX"
    host = XXX.XXX.XXX
    ```