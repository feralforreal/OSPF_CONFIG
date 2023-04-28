import napalm
import multiprocessing
import os
import csv
from datetime import datetime

print("=" *30)
print("Get Running-config from all routers and save them locally with timestamp by achieveing concurrency")
print("=" *30)

def get_config(hostname, username, password):

    x = napalm.get_network_driver('ios')
    optional_args = {'secret' : 'ngdb@1234'}
    device = x(hostname = i['hostname'], username = i['username'], password=i['password'], optional_args = optional_args)
    device.open()
    config = device.get_config(retrieve='running')
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    filename='{}_{}.txt'.format(device.hostname, timestamp)
    if device.hostname == '198.51.100.1':
        filename = 'R1{}.txt' .format(timestamp)
    elif device.hostname == '198.51.101.3':
        filename = 'R2{}.txt' .format(timestamp)
    elif device.hostname == '198.51.101.2':
        filename = 'R3{}.txt' .format(timestamp)
    else:
        filename = 'R4{}.txt' .format(timestamp)
    print(filename)
    with open (filename, "w") as f:
        f.write(config['running'])
    device.close()

if __name__ == "__main__":
    with open('ssh_login_Lab4.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        ssh_details = [dict(zip(headers, row)) for row in reader]
    d = []
    for i in ssh_details:
        p = multiprocessing.Process(target=get_config, args=(i['hostname'], i['username'], i['password']))
        d.append(p)
        p.start()
    for process in d:
        p.join()