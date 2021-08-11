# Usage of EXPMON Public APIs 

## Introduction

Please note by using the EXPMON Public APIs you're agreeing to our [Terms of Services](https://expmon.com/static/tos.pdf) and [Privacy Policy](https://expmon.com/static/privacy_policy.pdf). Basically, the principle is that we provide the service on a "AS IS" basis and we provide no warranty of any kind, and, **if you're not allowed to share the sample with us, please don't submit.**

You're highly recommended to read our [Introduction and FAQ](https://expmon.com/about/) first if you haven't done so.

If you have any questions when using the APIs, please feel free to email us at contact@expmon.com.

A free trial API key is provided as following:
>1111111111111111111111111111111111111111

The key is temporary and shared with all users, it may be revoked anytime. So, you'd better use a dedicated key, please email us at contact@expmon.com, it's free.



## Submit a file to EXPMON Public for analysis

**Url:** `https://expmon.com/api/public/file/submit`

**Input:**
* the file data
* the filename

**Output:**
* the SHA256 hash of the submitted sample

You're recommended to submit the in-the-wild filename (actually, only the extension name matters) in order to have a faster and better analysis.

Example Python code:

```Python
headers = {'Authorization': 'key %s' % key}
files = {'file_data': (sample_name, open(sample_path, 'rb'))}
response = requests.post(url, files = files, headers = headers)
```








## Query the analysis result by supplying the SHA256 hash

**Url:** `https://expmon.com/api/public/file/analysis/<sha256>`

**Input:**
* The sha256 hash returned when you use our submission API


**Output:**

There will be quite some outputs, depending on the submitted object. Usually, you will get:

- `resp['code']` for telling if the status of the analysis, the sample is still being analyzed, or finished normally (code=0), or something error occurred.

- `resp['detection']['result']` tells the analysis result classified by our system. There're 4 levels, "NoThreatDetected", "Informational", "Suspicious", and "Malicious".

  - **NoThreatDetected** - No threat detected in current configuration of our system
  - **Informational** - Usually mean we saw something in the sample but they're not immediate threats, more info provided in description
  - **Suspicious** - The sample is suspicious, you should be very careful, if the sample is not from a truly trusted source, we recommended not to open the sample, more info provided in description
  - **Malicious** - This is the highest level, usually means we have some confidence this is an exploit, more info provided in description
  
  `resp['detection']['description']` is a list of strings to describe what potential threats we found.

- Then, it's the `resp['system_analysis_detail']`, which is a dictionary object, it tells how many objects we found through analyzing your submission.

For every object (`obj`), it comes with the SHA256 hash (`obj['sha256']`), and the file type (`obj['type']`), as well as the "envirtment-binding analysis logs" (`obj['envlogs']`).

The `obj['envlogs']` is another dictionary, it may contain one or many environments, depending on the object type. For what the environment strings mean, please read our [About](https://expmon.com/about/) page and the current [System](https://expmon.com/public/system/) configuration page.

For every `envlog`, currently, we provide 4 types of logs, they are "FileAccess_Read", "FileAccess_Write", "RegAccess_Read", and "RegAccess_Write" logs.




**Example Python code:**

```Python
headers = {'Authorization': 'key ' % key}
response = requests.get(url, headers = headers)
resp = response.json()
```

## Demo code
The `expmon_api_demo.py` demonstrates how to submit a sample and wait for the detection result, once it gets the result, it will display the detection information on the screen, and write the "directory-like" organized information such as the  "found objects", the environment-binding analysis logs, in the current directory. Try it and you will know how all the things work.

Usage:
`python expmon_api_demo.py test.rtf`


## Some notes..

1. You should not query the analysis result within 30 seconds after you submit the sample, because our system needs at least 30 seconds to process a submission. Read our "About" page for more information.
2. Every call of our API will be counted in your quota. Currently, all issued API keys will have a maximum of 1000 submissions and 5000 queries per day. The quotas could be changed from time to time.
3. The analysis waiting time could be longer if there's more samples coming and when we have limited computing resources on our server side.
4. Our server at this time may not be stable, if you're waiting for too long for a simple sample, say, more than 15 minutes, it may indicate an error in our system or our system is not available at this moment, you may terminate the analysis result querying process in this situation  (and notify us via email or Twitter) . You may also want to submit a simple test file first if you're uploading a lot of samples at one time.

Finally, we hope you find our service useful! :-)


## License
Licensed GNU GENERAL PUBLIC LICENSE, Version 3, see https://github.com/EXPMON/PubAPIs/blob/master/LICENSE.md

Copyright (C) 2021 EXPMON Ltd.
