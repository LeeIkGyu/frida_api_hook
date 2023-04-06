import frida, os

from pathlib import Path
from androguard.core.bytecodes.apk import APK
from glob import glob
from time import sleep
from csv_write import api_data

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        return payload
    else:
        print(message)

def api_monitor(apk_list):
    detected = ""
    
    if "benign" in apk_list[0]:
        detected = "benign"
    else:
        detected = "malware"
    
    for apk in apk_list:
        try:
            os.system('adb install -t -r {}'.format(apk))

            apkf = APK(apk)
            PACKAGE_NAME = apkf.get_package()

            js_path = r"C:\Users\apk82\Desktop\payload.js"

            jscode = Path(js_path).read_text()

            device = frida.get_usb_device(1)
            pid = device.spawn(PACKAGE_NAME)
            session = device.attach(pid)
            sleep(1)

            script = session.create_script(jscode)
            script.on('message', on_message)
            script.load()

            api = script.exports
            api_list = api.apimonitor()

            os.system('frida-kill -U {}'.format(pid))
            os.system('adb uninstall {}'.format(PACKAGE_NAME))
        except:
            continue

        api_data(api_list, detected)
        sleep(1)

if __name__ == '__main__':
    benign_list = glob(r'D:\benign_apk(23.2)\\'+'*.apk')
    malware_list = glob(r'D:\malware_apk(16.6~23.3)\\'+'*.apk')
    
    # api_monitor(benign_list)
    api_monitor(malware_list)
