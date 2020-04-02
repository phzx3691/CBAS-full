# CBAS-full

Project using Particle mesh devices for environmental sensor streaming and Plotly/Dash for visualization.

## Resources

* Learning with Kaggle
  * [Kaggle - Python](https://www.kaggle.com/learn/python)
  * [Kaggle - Pandas](https://www.kaggle.com/learn/pandas)
  * [Kaggle - SQL intro](https://www.kaggle.com/learn/intro-to-sql)

* Docs
  * [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  * [TMUX](https://tmuxguide.readthedocs.io/en/latest/index.html)
  * [Dash/Plotly](http://dash.plotly.com/)
  * [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html#user-guide)
  * [TimescaleDB](https://docs.timescale.com/latest/introduction)
* Cheat Sheets
  * [Conda](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
  * [Tmux](https://tmuxcheatsheet.com/)
  * [Pandas](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
  
---

## Setup

We need to setup an isolated Python environment where the necessary libraries will be installed.
You can use either [Anaconda](https://docs.conda.io/projects/conda/en/latest/index.html) or [venv](https://docs.python.org/3/library/venv.html) for this, depending on the situation.

  1. Install:
     * Python 3+
     * Condas or virtual env
     * Github
       * Sould be using `dependable` branch
  2. Python libraries  
     1. [Anaconda](#Miniconda-Setup)
     2. [pip](#Pyenv-Setup)

     * If using `conda`, it is advised to install using `conda install` first, then `pip` for the `PyparticleIO` library.
     * For Python virtual environment just use `pip`
  
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

2. Run through prompts in set-up and once installed, restart terminal to finish.
  
3. *If you'd prefer that conda's base environment not be activated on startup:
  (This would be so conda does not auto-activate every time you start your terminal)

  ```bash
    conda config --set auto_activate_base false
  ```

### Creating conda environments

Once conda is installed and initialized, (You can do something like `conda activate` in the terminal) we want to create a new environment within our CBAS-full directory.

* [Docs.conda.io - Specifying a location for an environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment)

  :point_up: general information on environment locations

There are multiple ways to create our conda environment:

1. [Using environment.yml file](#environment-yml-file)
2. [Manual installation](#manual-install)
3. [Using spec-file.txt](#spec-file-txt) (Platform specific)

---

#### Environment yml file
  
1. Navigate to CBAS-full directory

2. Using evironment.yml

```bash
conda env create --prefix ./env --file environment.yml
```

3. Then install one more library:

* Instal PyparticelIO

```bash
pip install pyparticleio
```

---

Or

#### Manual install

1. Navigate to CBAS-full directory

* Create "vanilla" environment:
  
```bash
conda create ---prefix ./env
```

1. Activate the environment:

  ```bash
  conda activate ./env
  ```

2. Install libraries:

```bash
conda install pandas numpy glob2 dash tqdm scipy pymysql sqlalchemy psycopg2 PYparticleIO plotly dash jupyterlab
```

3. Then install one more library via pip:

* Instal PyparticelIO

```bash
pip install pyparticleio
```

---
Or

#### spec-file-txt

1. Create environment using spec-file[your platform].txt:
  (*only one for win_64 at this moment)

```bash
conda create ---prefix ./env --file spec-file[win_64].txt
```

2. To activate the environment:

```bash
conda activate ./env
```

3. Then install one more library via pip:

* Instal PyparticelIO

```bash
pip install pyparticleio
```

---
---

## Pyenv-Setup

If using venv:

```

venv installation
```

### pip installation

1. Activate virtual environment

2. Create environment from the requirements.txt file:
  
    ```bash
    pip install requirements.txt
    ```

---
---

Now all necessary software should be installed.:clap:  
*In order to run these scripts, you must have your virtual environment activated!*

Last step is to create a config file that keeps keys/credentials for scripts. This should be in the `.gitignore` file.

## Config-file

* Create `config.py`:
  
  In folders where script is running, either a `config.py` or `sqlconfig.py` is needed

  ```bash
  nano config.py
  ```

    Where you need the following:

    ```
    # .gitignore should include reference to config.py
    Particle_key = "XXXXXXXXXXXXXXXXXXX"
    user = "[USER]"
    passwd = "[PASSWORD]"
    host = XXX.XXX.XXX
    ```

`Particle_key` is only needed for ingestion script
`host` not needed yet  
This will be changed to just having the same file in the root directory of this repo later...
