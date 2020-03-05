# Running scripts on Linux

## Running multiple terminal sessions

### Tmux

Use Tmux to run multiple sessions in the terminal:  

Tmux instances are run from shared directory so multiple user can access  
      Tmux directory for shared sessions :

 ```bash
'/tmp/shareds'
 ```

To list open sessions (not from within session)  

```bash
tmux -S /tmp/shareds ls
```

To attach to session:

 ```bash
tmux -S /tmp/shareds attach -t [sessionName]
```

To detach from the session

```bash
Ctrl + B,D
```

# Plotly/Dash Scripts

## Ingestion script  ---  CBAS-full/Pub_Sub_ingestion/start.py

Since this script only works w Python 2  

1. New condas env with Python 2
2. Install [PyParticleIO](https://pypi.org/project/PyParticleIO/)

Create Python2.7 condas env

```bash

```

Install PyParticleIO 0.1.0  

```bash
pip install PyParticleIO
```

---

New Tmux session

```bash
tmux -a /tmp/shareds new -s ingest
```

---
Re-activate Condas env py2

---

list tmux sessions 

```bash
tmux -S /tmp/shareds ls
```


Attach to the ingestion session

```bash
tmux -S /tmp/shareds attach -t ingest
```

---

Go to directory for this script

```bash
cd ~/CBAS-Full/Pub_sub.../
```

Run script -

```bash
python2.7 start.py ~/CBAS-full/Plotly_dash/CSV/3Raw/From_Ingestio
ns/ingestions_BK/
```

If all is well...
![Ingestion Script Output](/png/Ingestion.jpg)

---

## Dash Live stream

Live Dash app for sensor data ingested using ingestion script  
CBAS-full/Plotly_dash/stable_scripts/Dash_apps/Ingestion_stream_Dash.py

To create a session

```bash
tmux -a /tmp/shareds new -s livestream
```

To attach to  the livestream session

```bash
tmux -a /tmp/shareds attach -s livestream
```

Go to directory

```bash
cd dashboard/Plotly-Dash/stable_scripts/Dash_apps/
```

Run script

```bash
python3 Ingestion_stream_Dash.py
```
