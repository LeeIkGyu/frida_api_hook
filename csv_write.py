import pandas as pd

def api_data(api_dataset, detected):
    data_set = {}

    api_list = ['android.os.Debug', 'android.content.ContentResolver', 'com.android.okhttp.internal.http.HttpURLConnectionImpl', 'android.app.ActivityThread', 'android.telephony.SmsManager', 'java.security.MessageDigest', 'dalvik.system.BaseDexClassLoader', 'android.app.ActivityManager', 'dalvik.system.DexFile', 'java.lang.ProcessBuilder', 'dalvik.system.PathClassLoader', 'android.telephony.TelephonyManager', 'android.app.ApplicationPackageManager', 'android.accounts.AccountManager', 'android.app.Activity', 'android.app.SharedPreferencesImpl', 'android.app.ContextImpl', 'java.net.URL', 'dalvik.system.DexClassLoader', 'android.util.Base64', 'java.io.FileInputStream', 'android.media.MediaRecorder', 'android.app.SharedPreferencesImpl$EditorImpl', 'android.os.Process', 'javax.crypto.spec.SecretKeySpec', 'android.net.wifi.WifiInfo', 'dalvik.system.InMemoryDexClassLoader', 'com.android.okhttp.internal.huc.HttpURLConnectionImpl', 'android.media.AudioRecord', 'android.app.NotificationManager', 'java.lang.Runtime', 'libcore.io.IoBridge', 'android.database.sqlite.SQLiteDatabase', 'org.apache.http.impl.client.AbstractHttpClient', 'android.content.BroadcastReceiver', 'android.location.Location', 'android.webkit.WebView', 'android.content.ContextWrapper', 'android.os.SystemProperties', 'android.content.pm.PackageManager', 'javax.crypto.Cipher', 'java.io.FileOutputStream', 'class']
    
    for api in api_list:
        for i in api_dataset:
            if api == i:
                data_set[api] = 1
    
    for api in api_list:
        if api in data_set:
            pass
        else:
            data_set[api] = 0
    
    if detected == 'malware':
        data_set['class'] = 'malware'
    else:
        data_set['class'] = 'benign'
        
    result = pd.DataFrame.from_dict([data_set])

    result.to_csv('api_dataset3.csv', header=False,index=False,mode='a')
