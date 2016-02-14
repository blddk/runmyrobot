import subprocess
import re
import os
import time
import urllib2
import platform



#ffmpeg -f qtkit -i 0 -f mpeg1video -b 400k -r 30 -s 320x240 http://52.8.81.124:8082/hello/320/240/


def handleDarwin():

    response = getVideoPort()
    print "video port:", response

    p = subprocess.Popen(["ffmpeg", "-list_devices", "true", "-f", "qtkit", "-i", "dummy"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    print err

    deviceAnswer = raw_input("Enter the number of the camera device for your robot from the list above: ")
    commandLine = 'ffmpeg -f qtkit -i %s -f mpeg1video -b 400k -r 30 -s 320x240 http://runmyrobot.com:8082/hello/320/240/' % deviceAnswer
    
    while(True):
        os.system(commandLine)
        print "Press Ctrl-C to quit"
        time.sleep(3)
        print "Retrying"
    
    print commandLine





def getVideoPort():

    cameraIDAnswer = raw_input("Enter the Camera ID for your robot, you can get it from the runmyrobot.com website: ")
    url = 'http://runmyrobot.com:3100/init_video_port/%s' % cameraIDAnswer
    print "GET", url
    response = urllib2.urlopen(url).read()

    return response




def handleWindows():

    p = subprocess.Popen(["ffmpeg", "-list_devices", "true", "-f", "dshow", "-i", "dummy"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    
    out, err = p.communicate()
    
    lines = err.split('\n')
    
    count = 0
    
    devices = []
    
    response = getVideoPort()
    print "video port:", response
    
    for line in lines:
    
        #if "]  \"" in line:
        #    print "line:", line
    
        m = re.search('.*\\"(.*)\\"', line)
        if m != None:
            #print line
            if m.group(1)[0:1] != '@':
                print count, m.group(1)
                devices.append(m.group(1))
                count += 1
    
    
    deviceAnswer = raw_input("Enter the number of the camera device for your robot from the list above: ")
    device = devices[int(deviceAnswer)]
    commandLine = 'ffmpeg -s 320x240 -f dshow -i video="%s" -f mpeg1video -b 400k -r 20 http://runmyrobot.com:8082/hello/320/240/' % device
    
    while(True):
        os.system(commandLine)
        print "Press Ctrl-C to quit"
        time.sleep(3)
        print "Retrying"
    
    print commandLine
    
    

if platform.system() == 'Darwin':
    handleDarwin()
elif platform.system() == 'Windows':
    handleWindows()
else:
    print "unknown platform", platform.system()



