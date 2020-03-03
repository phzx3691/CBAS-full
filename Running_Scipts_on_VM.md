# Running scripts on Linux


## Tmux

In the terminal use Tmux to run multiple sessions:  
      Tmux directory for shared sessions :  
      

To list open sessions (not from within session)  
      <pre><code> tmux -S /tmp/shareds ls  
      </code></pre>


To attach to session (while in the session):
      <pre><code> tmux -S /tmp/shareds attach -t [sessionName]
      </code></pre>
      
ctrl-B, d to detach from the session



### Ingestion script  ---  CBAS-full/Pub_Sub_ingestion/start.py
To create a session 
      <pre><code> tmux -a /tmp/shareds new -s ingest 
      </code></pre>
To attach to  the ingestion session
       <pre><code>tmux -a /tmp/shareds attach-s ingest
       </code></pre> 
      CD to directory for script 
cd ingest/sensor-feed/
Run script - 
~/ingest/sensor-feed$ “python start.py ~/dashboard/Plotly-Dash/CSV/3Raw/ingestions_BK”




### Live stream --- CBAS-full/Plotly_dash/stable_scripts/Dash_apps/Ingestion_stream_Dash.py 
To create a session 
       <pre><code>  tmux -a /tmp/shareds new -s livestream
       </code></pre>    
       
To attach to  the livestream session 
       <pre><code>tmux -a /tmp/shareds attach-s livestream
       </code></pre> 
Go to directory 
       <pre><code> cd dashboard/Plotly-Dash/stable_scripts/Dash_apps/
      </code></pre>
Run script
  <pre><code> python3 Ingestion_stream_Dash.py 
  </code></pre>




