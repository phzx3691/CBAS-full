# UNEP Sensor Feed

This is a python script for retrieving HOBO and Mote sensor data from the web.

# Requirements

- [Python 2.7](https://www.python.org/downloads/)
- Configured HOBO Sensor(s)
- Configured Mote Sensor(s)

## Usage

- `./start.py [OUTPUT_DIR]`
- For testing, replace [OUTPUT_DIR] with `csv/`
- To link with HaDatAc, replace [OUTPUT_DIR] with the full path of your `hadatac/unprocessed_csv/` folder
- You will be prompted for passwords to each of the linked accounts. Contact Marshall James if you need these, or change the respective accounts to your own.

## Sensor setup

Before you can begin retrieving data, each sensor must be set up to push the data to HOBOlink and Digi Device Cloud

### HOBO Sensors

You will need an MX series Hobo sensor, or an RX3000 or U30 Remote Monitoring Stations. This guide will focus on the MX series.

1. Create a [HOBOlink account](https://www.hobolink.com)
2. Download HOBOmobile onto a smart phone, and enable bluetooth.
3. Open the app, and go to the settings tab. Enter your account details on the HOBOlink section, and enable data uploading.
4. Go back to the HOBOs tab, and click on your sensor.
5. Once you've connected to your sensor, click "Readout".
    - You will need to do this whenever you want to push HOBO data
6. Login to HOBOlink. You should see the sensor under "Standalone Device Deployments"
7. Click on "Exports" and then "Create new export"
8. Enter the serial number for the sensor, and for export data put "over the past" and select how often you'd like hobo to attempt an export (rec. 15 minutes)
9. For part 2, select the sensor, and then click save.
10. Go to "Data Delivery" and then create a new delivery. Enter the same information for name and delivery time.
11. For data destination, click email, and input a valid gmail address.
    - It is recommended you create a gmail just for a sensor feed.
    - Go to [Less Secure Apps](https://myaccount.google.com/lesssecureapps) to allow desktop programs to access your gmail.
12. Click save. Now whenever you click "Readout" on your smart phone, the data will be emailed to your gmail account.

### Mote Sensors

[Kippkitts Sensor Mote](https://github.com/kippkitts/DataSensingLab/tree/master/DSL_Sensor_Mote)
