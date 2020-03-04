# Linux VM Environment Setup

How-to for setting up required libraries to run code  
Tested on Gcloud  Debian GNU/Linux, 10 (buster) image

## Resources

* [Condas Cheet Sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)

* [Tmux Cheat Sheet]()

### Setup VM

#### On Initial Boot 

* Update system

    ```bash
    Sudo apt-get update&&sudo apt-get update
    ```

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

* Run through set-up and Condas should be installed, restart terminal to finish


#### Creating an environment

Use CBAS-Full.yml to create new env

```bash
conda env create --file CBAS_Full.yml
```

#### Activate environment

```bash
conda env list
```
