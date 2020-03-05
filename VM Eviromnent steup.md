# Linux VM Environment Setup

How-to for setting up required libraries to run code  
Tested on Gcloud  Debian GNU/Linux, 10 (buster) image

## Resources

* [Conda Cheet Sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)

* [Miniconda Docs](https://docs.conda.io/en/latest/miniconda.html)

* [Tmux Cheat Sheet](https://tmuxcheatsheet.com/)

* [TMUX guide](https://tmuxguide.readthedocs.io/en/latest/index.html)

### Setup VM

#### On Initial Boot

* Update system

    ```bash
    sudo apt-get update&&sudo apt-get upgrade

* Install wget

    ```bash
    sudo apt-get install wget
    ```

* Install Git

    ```bash
    sudo apt-get install git
    ```

Clone CBAS-Full Git Repo

```bash
git clone https://github.com/phzx3691/CBAS-full.git
```

#### Download and install Miniconda

* Download latest version of Miniconda here:  
https://docs.conda.io/en/latest/miniconda.html

    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
    ```

* Then run the installation script:

    ```bash
    bash Miniconda2-latest-Linux-x86_64.sh
    ```

* Run through set-up and Condas should be installed, restart terminal to finish install

If you'd prefer that conda's base environment not be activated on startup:  

```bash
    conda config --set auto_activate_base false
```



#### Creating environments

Use environment.yml to create new env

```bash
conda env create --file environment.yml
```

Create new Py2 env for ingestion script

---

```bash
conda env create --name py2 python=2.7
```

---
