# Linux VM environment setup

How-to for setting up required software/libraries to run code  
Tested on Gcloud  Debian GNU/Linux, 10 (buster) image

## Resources

* [Conda Cheet Sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)

* [Miniconda Docs](https://docs.conda.io/en/latest/miniconda.html)

* [Tmux Cheat Sheet](https://tmuxcheatsheet.com/)

* [TMUX guide](https://tmuxguide.readthedocs.io/en/latest/index.html)

---

## VM setup

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
wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
```

* Then run the installation script:

```bash
bash Miniconda2-latest-Linux-x86_64.sh
```

* Run through set-up and Condas should be installed, restart terminal to finish install

* If you'd prefer that conda's base environment not be activated on startup:  

```bash
conda config --set auto_activate_base false
```

---

### Creating Conda Environments

### Default Python3 Conda env for Plotly/Dash (CBAS-Full)

Use environment.yml to create new default env using required libraries  
This should be the env used for Plotly/Dash scripts  

* To create new env from environment.yml

```bash
conda env create --file environment.yml
```

This env has all necessary libraries to run /stable_scripts and is already named "CBAS-Full"

*** 

### Default Python2 Conda env for Ingestion Script (Py2)

As the Ingestion script uses a library that requires Python2, (PYparticleIO) we need a seperate conda env with Python2.7

* To create new Py2 env for ingestion script

```bash
conda env create --name py2 python=2.7
```

In order to install libraries in Python2.7, it may be necessary to install pip2.7 
I had to do this because Py3 seems to be the default 'python' PATH

There should be a binary called "pip2.7" installed at some location included within your $PATH variable.

You can find that out by typing

```bash
which pip2.7
```

This should print something like '/usr/local/bin/pip2.7' to your stdout. If it does not print anything like this, it is not installed. In that case, install it by running:

```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python2.7 get-pip.py
```

Now, you should be all set, and

```bash
which pip2.7
```

should return the correct output.

Now you should be able to install PYparticleIO/pandas/numpy  
these are the libraries needed to run ingestion

```bash
pip2.7 install PYparticleIO
```

```bash
pip2.7 install pandas&&pip2 install numpy
```

---

