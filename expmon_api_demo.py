import os
import sys
import time
import zlib
import codecs
import shutil
import requests



expmon_key = '1111111111111111111111111111111111111111'


url_submission = 'https://expmon.com/api/public/file/submit'
url_query_prefix = 'https://expmon.com/api/public/file/analysis/'





sample_path = sys.argv[1]
sample_name = os.path.basename(sample_path)


#sample submission, key is in HTTP Header
headers = {'Authorization': 'key %s' % expmon_key}
files = {'file_data': (sample_name, open(sample_path, 'rb'))}
response = requests.post(url_submission, files = files, headers = headers)
resp = response.json()


if resp['code'] != 0:
    print('SOMETHING ERROR: %s' % resp['message'])
    exit(-1)

print('[INFO] Server returned message: ' + resp['message'])
sample_sha256 = resp['sha256']
print('[INFO] Submitted sample hash: ' + sample_sha256)




#continue to check until the server returns analysis result
while 1:
    time.sleep(30)
    headers = {'Authorization': 'key %s' % expmon_key}
    response = requests.get(url_query_prefix + sample_sha256, headers = headers)
    resp = response.json()

    #code -1 means sample is being analyzed
    if resp['code'] == -1:
        print('[INFO] Sample is being analyzed, wait additional 30 seconds')
    #code 0 means we get the result
    elif resp['code'] == 0:
        break
    else:
        print('UNKNOWN ERROR: %s' % resp['message'])
        exit(-1)




folder_root = sample_sha256
if os.path.exists(folder_root):
    print('[INFO] directory already exists, removing it.')
    shutil.rmtree(folder_root)
os.makedirs(folder_root)



system_analysis_detail = resp['system_analysis_detail']

print('Detection Result: ' + resp['detection']['result'])
print('Detection Description: ' + str(resp['detection']['description']))


for obj in system_analysis_detail:

    obj_folder_name = '%s__%s' % (obj['sha256'], obj['type'])
    folder_object = os.path.join(folder_root, obj_folder_name)

    os.makedirs(folder_object)

    for env_name in obj['envlogs']:

        folder_object_env = os.path.join(folder_object, env_name)
        os.makedirs(folder_object_env)

        for log_type in obj['envlogs'][env_name]:

            log_data_hexstr = obj['envlogs'][env_name][log_type]
            if log_data_hexstr == '' or log_data_hexstr == None:
                continue

            #log data is hex string in the traffic and is compressed
            log_data = zlib.decompress(codecs.decode(log_data_hexstr, 'hex'))
            
            #dump log data to file
            log_file_name = os.path.join(folder_object_env, log_type + '.txt')
            open(log_file_name, "wb").write(log_data)

