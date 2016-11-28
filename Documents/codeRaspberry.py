import RPi.GPIO as GPIO
import socket
from threading import Thread
import sys
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText




def SendMail():
	msg = MIMEMultipart()
	msg['From'] = 'info@georgesecurity.me'
	msg['To'] = 'simon@ponchau.eu'
	msg['Subject'] = 'Alerte' 
	message = 'Votre robot a detecter une alerte!!'
	msg.attach(MIMEText(message))
	mailserver = smtplib.SMTP('mail.privateemail.com', 587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
	mailserver.login('info@georgesecurity.me', 'ge0rge5')
	mailserver.sendmail('info@georgesecurity.me', 'simon@ponchau.eu', msg.as_string())
	mailserver.quit()




s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host= '127.0.0.1'
port=int(62900)
global speed
speed = 20 #vitesse de base
global data
global speedM1
global speedM2
distance=0
data = ''


s.bind(('',port))

GPIO.setmode (GPIO.BOARD)
#M1 Right Side

GPIO.setup (11, GPIO.OUT) #M1_AV
GPIO.setup (13, GPIO.OUT) #M1_AR
#M2 Left Side
GPIO.setup (15, GPIO.OUT) #M2_AV
GPIO.setup (12, GPIO.OUT) #M2_AR
#PWM
GPIO.setup (33, GPIO.OUT) #EN1 PWM
GPIO.setup (35, GPIO.OUT) #EN2 PWM

hz = 500 # frequence
global motor1
global motor2
motor1 = GPIO.PWM(33, hz)
motor2 = GPIO.PWM(35, hz)


motor1.start(0)
motor2.start(0)


class Listener(Thread):
	
    def run(self):
		while 1:
			global data
			print("test0")
			s.listen(1)
					
			conn,addr =s.accept()

			print (conn,addr)
			data=conn.recv(100000)
			data=data.decode("utf-8")
			print("output : %s " %data)
				

class Controller(Thread):
	
    def run(self):
		while 1:
			global data
			global speedM1
			global speedM2
			global speed
			global motor1
			global motor2
		#MODE AUTO
			
			if data == 'auto':
				print("test1")
				#http://www.raspberrypi-spy.co.uk/archive/python/ultrasonic_1.py --> ULTRASONIC SENSOR
				speedM1 = speed
				speedM2 = speed
				Auto()
			
		#MODE MANUEL
			else:
				print("output2 : %s " %data)
				

				if data=='up':
					Stop()
					GPIO.output(11, True)
					GPIO.output(15, True)


				if data=='down':
					Stop()
					GPIO.output(13, True)
					GPIO.output(12, True)

				if data=='left':
					Stop()
					
					GPIO.output(15, True)
			

				if data=='right':
					Stop()
					
					GPIO.output(11, True)
				
					
				if data=='stop':
				
					Stop()
					
				s.close
				
				
class Alert(Thread):
    def run(self):
		liste = []
		j = 0
		
		while 1:
		
		
			GPIO_TRIGGER = 23
			GPIO_ECHO    = 24
			GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
			GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
			GPIO.output(GPIO_TRIGGER, False)
			print("test2")
			# Allow module to settle
			time.sleep(0.5)

			# Send 10us pulse to trigger
			GPIO.output(GPIO_TRIGGER, True)
			time.sleep(0.00001)
			GPIO.output(GPIO_TRIGGER, False)
			start = time.time()
			print("test3")
			while GPIO.input(GPIO_ECHO)==0:
				start = time.time()

			while GPIO.input(GPIO_ECHO)==1:
				stop = time.time()
			print("test4")
			# Calculate pulse length
			elapsed = stop-start

			# Distance pulse travelled in that time is time
			# multiplied by the speed of sound (cm/s)
			distance = elapsed * 34300

			# That was the distance there and back so halve the value
			distance = distance / 2
		
		
			if data=='stop' or data=='':
				liste.append(distance)
				print("distance : %d " %distance)
				print ("j : %d " %j)
				if j>0 :
					if (liste[j-1]-liste[j])>20 :
						SendMail()
						print ('alert')
				
				if j > 100 : 
					j=0
				
				j+=1
				
				
				
				
			
list = Listener()
control = Controller()
alert = Alert()

'''list.daemon = True
control.daemon = True
alert.daemon = True '''

list.start()
control.start()
alert.start()
############################################################################			

def Accelerate():
	global speed
	if speed < 100:
		speed+=5
		time.sleep(0.1)
###########################################################################

def Stop():
	GPIO.output(11, False)
	GPIO.output(13, False)
	GPIO.output(15, False)
	GPIO.output(12, False)

###########################################################################
def Auto():
	GPIO_TRIGGER = 23
	GPIO_ECHO    = 24
	GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
	GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
	GPIO.output(GPIO_TRIGGER, False)
	print("test2")
	# Allow module to settle
	time.sleep(0.5)

	# Send 10us pulse to trigger
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	start = time.time()

	while GPIO.input(GPIO_ECHO)==0:
		start = time.time()

	while GPIO.input(GPIO_ECHO)==1:
		stop = time.time()

	# Calculate pulse length
	elapsed = stop-start

	# Distance pulse travelled in that time is time
	# multiplied by the speed of sound (cm/s)
	distance = elapsed * 34300

	# That was the distance there and back so halve the value
	distance = distance / 2

	if distance < 65:
		Stop()
		time.sleep(2)
		GPIO.output(15, True)
		time.sleep(0.5)


	else:
		Stop()
		GPIO.output(11, True)
		GPIO.output(15, True)


