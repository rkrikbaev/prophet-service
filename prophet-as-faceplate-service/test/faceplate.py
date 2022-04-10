import os, time
import datetime
import json


JSON = '''{
    "metadata": {
        "point": "shym-4", 
        "type": "prophet",
        "settings":{
            "growth": "linear",
            "changepoint_prior_scale": 30,
            "seasonality_prior_scale": 35,
            "interval_width": 0.98,
            "daily_seasonality": false,
            "weekly_seasonality": false,
            "yearly_seasonality": false,
            "seasonality": [
                {
                    "name": "hour",
                    "period": 0.0417,
                    "fourier_order": 5
                }
            ]
        }
    },
    "history": [[1626159114000, 46.46659429239697, 33.865], [1626162714000, 50.38077545566983, 33.135], [1626166314000, 49.786295583493974, 33.0], [1626169914000, 52.30600325119654, 33.0], [1626173514000, 49.74017713527362, 32.135], [1626177114000, 26.507367125644155, 32.0], [1626180714000, 20.825400896539158, 31.135], [1626184314000, 16.641573343804414, 30.135], [1626187914000, 12.88365472938776, 28.27], [1626191514000, 13.03941161652353, 27.135], [1626195114000, 12.865383213700188, 26.135], [1626198714000, 23.0075885798094, 26.0], [1626202314000, 29.750946025369963, 26.0], [1626205914000, 30.36831248536057, 25.135], [1626209514000, 28.746051325005425, 24.135], [1626213114000, 26.06918637600051, 23.135], [1626216714000, 27.71889996848636, 23.0], [1626220314000, 27.61792646200975, 23.0], [1626223914000, 29.282521453022955, 22.135], [1626227514000, 27.6570642212926, 24.595], [1626231114000, 29.47211756398148, 26.73], [1626234714000, 20.901465210812887, 28.73], [1626238314000, 19.566893250178232, 29.865], [1626241914000, 20.06650195276843, 30.865], [1626245514000, 19.581432925954925, 31.0], [1626249114000, 19.763265444149177, 31.865], [1626252714000, 20.146312865931193, 32.865], [1626256314000, 19.499077251661088, 33.865], [1626259914000, 20.496050887058047, 33.135], [1626263514000, 19.918877556726137, 33.0], [1626267114000, 19.885642845565478, 32.135], [1626270714000, 14.614254379067686, 31.135], [1626274314000, 12.052995100595156, 30.135], [1626277914000, 12.075608591365814, 29.135], [1626281514000, 11.714862450722588, 27.27], [1626285114000, 22.17041537279129, 24.405], [1626288714000, 29.7315270995956, 22.27], [1626292314000, 27.034812883857093, 21.135], [1626295914000, 30.357443650132815, 19.27], [1626299514000, 30.623968757263288, 19.0], [1626303114000, 29.982753248142135, 18.135], [1626306714000, 30.91508703640832, 18.0], [1626310314000, 31.083123297907484, 17.135], [1626313914000, 32.9891217580737, 17.0], [1626317514000, 28.84762504017565, 20.46], [1626321114000, 25.25211722192711, 21.0041067761807], [1626324714000, 23.6941498622534, 20.46], [1626328314000, 22.01953280939939, 10]], 
    "future": [[1626321114000, 19.27],[1626321115000, 19.27],[1626321116000, 66.1]]
}
'''

message = JSON.replace("\n", "") + "\n"

gt = datetime.datetime.now()
print('Request at {0}'.format(gt))

# message = 'Data from client at {0}\n'.format(gt)

# uncomment if read/write from/to by filename
# pw = os.open("pipeTo", os.O_RDWR | os.O_CREAT) #pipe client - > server
# pr = os.open("pipeFrom", os.O_RDONLY | os.O_CREAT) #pipe server - > client

# uncomment if read/write from/to by filedescriptor
# Create a pipe. Return a pair of file descriptors (r, w) usable for reading and writing, respectively.
os.pipe()

writesBytes = os.write(4, bytes(message, 'utf-8'))
# print(writesBytes)

# wait for response 60 sec
time.sleep(1)

# uncomment if read/write from/to by filename
# resp = os.read(pr,1000)
# rf = os.fdopen(pr, 'rb', 0)
# resp = rf.readlines()
# print(resp)

# uncomment if read/write from/to by filedescriptor
# 'metadata', 'prediction', 'anomalies'
i=0
content = b''

rf = os.fdopen(3)
# content = rf.readline()

while True:
    try:
        content = rf.readline()
        i +=1
        print('wait: ', i)
        if content is not None:
            content = json.loads(content)
            print(content)
            if {'metadata', 'prediction', 'anomalies'} <= set(content):
                print(content)
                break
        time.sleep(10)  
        print('next')          
    except OSError as exc:
        pass

print(content)
os.close(pw)
# os.close(pr)