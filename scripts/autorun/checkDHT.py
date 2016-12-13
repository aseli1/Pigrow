
script = 'chechDHT.py'
import os, sys
import datetime
import Adafruit_DHT
sys.path.append('/home/pi/Pigrow/scripts/')
import pigrow_defs
loc_dic = pigrow_defs.load_locs("/home/pi/Pigrow/config/dirlocs.txt")
set_dic = pigrow_defs.load_settings(loc_dic['loc_settings'], err_log=loc_dic['err_log'],)
#print set_dic


def read_and_log():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, set_dic['gpio_dht22sensor'])
        if humidity is not None and temperature is not None:
            timno = datetime.datetime.now()
            with open(loc_dic['loc_dht_log'], "a") as f:
                line = str(temperature) + '>' + str(humidity) + '>' + str(timno) + '\n'
                f.write(line)
            return humidity, temperature, timno
    except:
        print("--problem reading sensor--")
        return '-1','-1','-1'

def heater_control(temp):
    #checks to see if current temp should result in heater on or off
    templow  = set_dic['heater_templow']
    temphigh = set_dic['heater_temphigh']
    if temp < templow:
        message = "It's bloody cold"
        write_log(script, message)
    elif temp > temphigh:
        message = "fucking 'ell it's well hot in here"
        write_log(script, message)
    else:
        message = "This is a nice temperateure, no it is, don't you think?"
        print(" --not worth logging but, " + message)


hum, temp, timno = read_and_log()
heater_control(temp)