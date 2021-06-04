import sys
import os
import json



def get_list(network_name):
    network_info = os.system("docker network inspect {}".format(network_name))
    info = json.read(network_info)
    
    containers = info[0]["Containers"]
    services = dict()
    for _, container in containers.items():
        service_name = container['name'].split('.')[0]
        address = container['IPv4Address'].split('/')[0]
        if service_name not in services:
            services[service_name] = []
        services[service_name].append(address)
    return services


def gen_config():
    pass


if __name__ == '__main__':
    print(get_list(sys.argv[1]))
