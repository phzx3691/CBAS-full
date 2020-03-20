import pymysql
import sqlconfig
import pandas as pd
import sqlalchemy



passwd = sqlconfig.passwd
user = sqlconfig.user






connection = pymysql.connect(host=34.67.192.90,
      user=root,password=CEA299792458,
      db=sample)

c = connection.cursor()


c.execute(CREATE TABLE CARS (Brand text, Price number))
conn.commit()

Cars = {Brand: [Honda Civic,Toyota Corolla,Ford Focus,Audi A4],
        Price: [22000,25000,27000,35000]
        }

df = DataFrame(Cars, columns= [Brand, Price])




import pymysql
import sqlconfig
import pandas as pd
import sqlalchemy



passwd = 'CEA299792458'
user = 'postgres'
DB = 'newlab'


engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+passwd+'@localhost/'+DB)


base_path = os.path.dirname(os.path.dirname(os.path.abspath(os. getcwd())))
'/home/sheldon'

start_path = os.path.join(base_path,"dashboard","Plotly_dash","CSV", "1Processed","1234")
start_path



fn = 'protoCBAS-*'
path = sorted(glob.glob(os.path.join(start_path, fn)))
path

upload.to_sql('pet',engine,
    if_exists='append',
    index=False
)
