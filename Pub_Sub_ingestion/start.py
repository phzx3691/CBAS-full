#!/usr/bin/env python
import sys
import signal
import time
import particle

def main():

  def signal_handler(signal, frame):
    print("\nStopping collection.")
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)

  if len(sys.argv) < 2:
    print("Usage: python start.py [OUTPUT_DIR]")
    sys.exit(1)

  output_dir = sys.argv[1]

  p = particle.Particle(output_dir)
  p.login()

  while(True):
    time.sleep(15)

if __name__ == "__main__":
  main()

