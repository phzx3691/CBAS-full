
import pymysql






connection = 
      pymysql.connect(host='34.67.192.90',
      user='root',password='CEA299792458',
      db='sample')

c = connection.cursor()


c.execute('CREATE TABLE CARS (Brand text, Price number)')
conn.commit()

Cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
        'Price': [22000,25000,27000,35000]
        }

df = DataFrame(Cars, columns= ['Brand', 'Price'])