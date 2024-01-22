Simulation Code (Without Hardware):

	On Windows, Follow These Steps:
		1. Right Click "requirements-Windows.ps1" (ONLY ONCE!!)
		2. Select "Run With PowerShell Option"

		3. Right Click "initialize-Windows.ps1" (ONLY ONCE!!)
		4. Select "Run With PowerShell Option"
		5. Enter Your Email, And App Password Generated (YouTube Video For Reference https://www.youtube.com/watch?v=lSURGX0JHbA)

		6. Right Click "startserver-Windows.ps1"
		7. The Browser Automatically Opens The Link.
	
	On Linux, Follow These Steps:
		1. Double Click "requirements-Linux.sh" (ONLY ONCE!!)
		2. Double Click "initialize-Linux.sh" (ONLY ONCE!!)
		3. Enter Your Email, And App Password Generated (Same As Windows Method, use YouTube Video)
		4. Double Click "startserver-Simulation-Linux.sh" 


Actual Code (With Hardware): (LINUX ONLY)
	Properly Connect Your DHT22 and ZFM-20 Fingerprint Sensors, as well as your Buzzer.
	PINOUT: (Use Online Pinout to see which pin matches below number)
		Buzzer = Board Pin D18
		DHT22 = Board Pin D4
		
		ZFM-20 = Board Pin TX to Sensor RX
			 Board Pin RX to Sensor TX
		
	Follow These Steps:
		1. Double Click "requirements-Linux.sh" (ONLY ONCE!!)
		2. Double Click "initialize-Linux.sh" (ONLY ONCE!!)
		3. Enter Your Email, And App Password Generated (Same As Windows Method, use YouTube Video)
		4. Double Click "startserver-Linux.sh"