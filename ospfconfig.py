import multiprocessing
import os
import csv
import napalm

with open('ospf_config.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    ospf_details = [dict(zip(headers, row)) for row in reader]

x = napalm.get_network_driver('ios')
optional_args = {'secret': 'ngdb@1234'}

print("=" * 30)
print("Lab4_DevOps_SSH_Login_by_achieving_concurrency")
print("=" * 30)

def configure_ospf(router_details):
    try:
        device = x(hostname=router_details['hostname'], username=router_details['username'], password=router_details['password'], optional_args=optional_args)
        device.open()
        device.get_facts()
        device.load_merge_candidate(config='router ospf ' + router_details['process_id'] + '\n' +
                                               'network '  + ' ' + router_details['area_id'] + '\n')
        diffs = device.compare_config()
        if len(diffs) > 0:
            device.commit_config()

            print("OSPF configuration applied to" + router_details['hostname'])
        else:
            print("No OSPF configuration changes required on" + router_details['hostname'])
    except Exception as e:
        print("Error configuring OSPF on" + router_details['hostname'] + " : " + str(e))

i = []
with open('ospf_config.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    ssh_details = [dict(zip(headers, row)) for row in reader]

for router_details in ssh_details:
    p = multiprocessing.Process(target=configure_ospf, args=(router_details,))
    i.append(p)
    p.start()

for process in i:
    process.join()