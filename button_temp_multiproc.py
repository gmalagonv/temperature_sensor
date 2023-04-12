#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:23:11 2022

@author: gerard
"""
# copy to raspberry by ssh: 
# scp ~/nextcloud/python_stuff/raspberry/temperature_sensor/button_temp_multiproc.py gerard@192.168.0.145:~/python_stuff/button_temp_multiproc.py
# confirm rasberry's ip address by: ifconfig -a


#import threading
import multiprocessing
import time
import datetime
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import os
import glob
import xlsxwriter
from ctypes import c_bool
from oled_text import simple_text

## variables
delay = 10 # in seconds
save_after = 50
saveFile_flag = False

####
######
def read_temp_raw():
    # for temp sensor___________________________________________________
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    
    device_file = device_folder + '/w1_slave'
    #_____________________________________________________
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines



def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c#, temp_f
    


def print_temp(switchsensor, times, temps):
    # global switchsensor

    global delay
    global save_after
    count = 0

    while True:        
        if switchsensor.value: #and switchsensor != switchsensor_prev:
            #timer.set()
                        
            if count == 0:
                time_start = time.time()
                
            time_measure = time.time() - time_start
            temp = read_temp()
            print(time_measure, temp)
            # OLED SCREEN PRINT
            simple_text((str(temp) + '°C'), 20, 2, 'c',"sample #", 9, 80,'t', str(count), 15, 90, 'b')
            # simple_text("22°C", 22, 10, 'c', "sample #", 10, 70,'t', '1', 15, 85, 'b')
            times.append(time_measure)
            temps.append(temp)
            
            if count >= save_after and count % save_after == 0 and saveFile_flag:
                write_excel(times, temps, True)  
            count += 1
            
            time_run = count*delay - (time.time() -  time_start)
            #print(time_run)
            time.sleep(time_run)     
         
        else:
            #return
            count = 0
            
       
def button(switch_counter, switchsensor):
    #__________________________
    GPIO.setmode(GPIO.BOARD)
    # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #________________________________

    prev_input = 0
    while True:
        input = GPIO.input(10)
        if (not prev_input) and input:                
            switch_counter.value += 1
            switchsensor.value = ((switch_counter.value % 2) != 0)
            #print(switchsensor.value)
            # if switchsensor:
            #     time_start = time.time()
            # elif not switchsensor and switch_counter > 1:
            #     t2.start()
                #signal.pause() 
                #os.kill(os.getpid(), signal.SIGINT)
            
        prev_input = input
        time.sleep(0.05)
        
def write_excel(times, temps, auto_flag):
    now = datetime.datetime.now()
    name = 'temp_' + str(now.year) +'_' + str(now.month) + '_' + str(now.day) +'_' + str(now.hour) +'_' + str(now.minute) + '.xlsx'
        
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    for idx, n in enumerate(times):
        worksheet.write(idx, 0, times[idx])
        worksheet.write(idx, 1, temps[idx])
    workbook.close()
    
    if auto_flag:        
        print('file saved automatically')
        simple_text('file saved', 16, 20, 't', 'automatically!', 16, 5, 'b')

    else:
        print('file saved')
        simple_text('STOPPED', 22, 14, 'c')
        time.sleep(2)
        simple_text('file saved!', 18, 19, 't', 'press button to restart', 10, 8, 'b')

        
if __name__ == "__main__":
    switch_counter = multiprocessing.Value('i', 0)
    switchsensor = multiprocessing.Value(c_bool, False)

    manager = multiprocessing.Manager()
    times = manager.list()
    temps = manager.list()

    t1 = multiprocessing.Process(target=button, args= (switch_counter, switchsensor, ) )    
    t2 = multiprocessing.Process(target=print_temp, args= (switchsensor, times, temps, ) )

    t1.start()    
    #while not switchsensor:
    simple_text('press button to start', 10, 8, 'c')

    t2.start()
    terminated = False
    #e
    while True:     

        
        if switchsensor.value == False and switch_counter.value > 1 and terminated == False:
            t2.terminate()
            if saveFile_flag:
                write_excel(times, temps, False)            
            
            times = manager.list()
            temps = manager.list()
            terminated = True           
            
        elif terminated == True and switchsensor.value == True:
            t2 = multiprocessing.Process(target=print_temp, args= (switchsensor,  times, temps, ) )
            t2.start()
            
            print('restarted')
            terminated = False

  



