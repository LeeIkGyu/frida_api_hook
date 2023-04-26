import frida, os

from pathlib import Path
from androguard.core.bytecodes.apk import APK
from glob import glob
from time import sleep
from csv_write import api_data

def on_message(message, data):
    if message['type'] == 'send':
        # api list를 return 함
        payload = message['payload']
        return payload
    else:
        print(message)

def api_monitor(apk_list):
    detected = ""
    
    # 샘플 apk가 정상인지 악성인지 확인
    if "benign" in apk_list[0]:
        detected = "benign"
    else:
        detected = "malware"
    
    for apk in apk_list:
        try:
            # 에뮬레이션에 샘플 파일 설치
            os.system('adb install -t -r {}'.format(apk))

            # 샘플 파일의 패키지 명을 가져 옴
            apkf = APK(apk)
            PACKAGE_NAME = apkf.get_package()

            # frida script 경로 지정
            js_path = r"C:\Users\apk82\Desktop\payload.js"
            # frida script를 가져 옴
            jscode = Path(js_path).read_text()

            # frida 연결 후 샘플 파일 실행
            device = frida.get_usb_device(1)
            pid = device.spawn(PACKAGE_NAME)
            session = device.attach(pid)
            sleep(1)

            # frida script 실행
            script = session.create_script(jscode)
            script.on('message', on_message)
            script.load()

            # on_message 함수에서 api list를 return 받음
            api = script.exports
            api_list = api.apimonitor()

            # 샘플 파일 실행 종료
            os.system('frida-kill -U {}'.format(pid))
            # 샘플 파일 삭제
            os.system('adb uninstall {}'.format(PACKAGE_NAME))
        except:
            continue
        
        # api 목록들을 csv 형태로 저장
        api_data(api_list, detected)
        sleep(1)

if __name__ == '__main__':
    # 샘플 파일들의 경로를 읽어 옴
    benign_list = glob(r'D:\benign_apk(23.2)\\'+'*.apk')
    malware_list = glob(r'D:\malware_apk(16.6~23.3)\\'+'*.apk')
    
    # api 추출 시작
    api_monitor(benign_list)
    api_monitor(malware_list)
