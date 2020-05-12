#Modules
import subprocess
from flask import *
import platform
import time
from jinja2 import *
from jinja2.loaders import FileSystemLoader
#--------------------------------------------------------------------------------#
#End Result (Core)
#Webpage with button to request if system (My Main Windows System) is up / down 
#Timestamp

#Optional:
#Other Infos (IP/MAC Address with nmap, OS)
#SQL DB with all requests
#       run webpage on raspberry pi
#               Site Protection
#                SSecure Connection / Encryption
#Android App (APK)
#Mutiple Systems (or whole network with nmap)
#--------------------------------------------------------------------------------#
#Definitions
pc_state = []
rtime = []

#Code Block 1: Check if system is up through pinging system and print output (on- or offline) 
#Possible Issue: No response to ping eventhough system up (nmap workaround?)

#Ping-Function
def ping_exec (form_text):
        #Some extra stuff
        global pc_state
        global rtime
        target = form_text
        tstamp = time.gmtime()
        rtime = time.strftime("%d-%m-%Y %H:%M:%S", tstamp)

#Functions
#--------------------------------------------------------------------------------------------
        def win_ping(target):  
                global pc_state
                #Ex.: ping -n 1 192.168.A
                win_cmd = subprocess.run(['ping', "-n", '1', target], capture_output=True)
                answer = win_cmd.stdout.decode()
                if "Destination host unreachable" in answer:
                        pc_state = "System is down..."
                else:
                        pc_state = "System is up!"
                return pc_state
                
        
        def ping(target):                           
                #Ex.: ping -c 1 192.168.A.BCD
	        cmd = ['ping', '-c', '1', target]	
	        return subprocess.run(cmd).returncode == 0        
#-----------------------------------------------------------------------------------------------------------------------------------------------------
        
        #Executes Function
        current_os = platform.system().lower()
        if current_os == 'windows':
                win_ping(target)

        elif current_os == 'linux':
                ping(target)
                if ping(target) is True:
                        pc_state = "System is up!"
                else:
                        pc_state = "System is down..."
       
        else:
                ping(target)
                if ping(target) is True:
                        pc_state = "System is up!"
                else:
                        pc_state = "System is down..."
        return pc_state, rtime       


#Code Block: Web Implementation (Flask)

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
        form_text = request.form['text']
        log = ping_exec(form_text)
        return render_template('result.html', ip_t = form_text, pc_end = str(log[0]), start_time = str(log[1]))


if __name__ == "__main__":
    app.run(host='192.168.1.154')