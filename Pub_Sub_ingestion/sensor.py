import time
import math

class Sensor:

  def __init__(self, output_dir):
    self.output_dir = output_dir
    self.sensors = {}
    self.sensors_registered = False

  def getCurrentTime(self, space=True, day=False, fifteen=False):
    if day:
      return time.strftime("%Y-%m-%d", time.gmtime())
    elif fifteen:
      unrounded = time.strftime("%Y-%m-%dT%H:%M", time.gmtime())
      minute = float(unrounded[-2:])
      rounded = unrounded[:-2] + str(int(math.floor(4*(minute/60))*15))
      return rounded
    elif space:
      return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    else:
      return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

  def log(self, m_type, message):
    timestring = self.getCurrentTime()
    print("[{}]({}) {}".format(m_type, timestring, message))
   
