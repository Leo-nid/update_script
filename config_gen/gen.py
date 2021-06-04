import sys
import os
import json


def add_tabs(string, level):
    return ' ' * level * 2 + string


def format_config(dct, level=-1):
    if type(dct) == list:
        return '\n'.join([format_config(item, level + 1) for item in dct])
    elif type(dct) == tuple:
        if type(dct[1]) in (list, dict):
            return add_tabs('{} {{\n{}\n'.format(dct[0], format_config(dct[1], level)), level) + add_tabs('}', level)
        else:
            return add_tabs('{} {};'.format(dct[0], dct[1]), level)
    elif type(dct) == dict:
        return format_config(list(dct.items()), level)
    return str(dct)


def get_list(network_name):
    network_info = os.popen("docker network inspect {}".format(network_name)).read()
    info = json.loads(network_info)
    
    containers = info[0]["Containers"]
    services = dict()
    for _, container in containers.items():
        service_name = container['Name'].split('.')[0]
        address = container['IPv4Address'].split('/')[0]
        if service_name not in services:
            services[service_name] = []
        services[service_name].append(address)
    return services



def gen_config(services):
    config = dict()
    config['http'] = []
    config['worker_processes'] = 2
    config['events'] = {'worker_connections':4096}
    for name, servers in services.items():
        config['http'].append(('upstream {}'.format(name), [('server', '{}'.format(server)) for server in servers]))
        serv_info = dict()
        serv_info['listen'] = 80
        serv_info['server_name'] = name + '.local'
        serv_info['location /'] = [('proxy_pass', 'http://{}'.format(name))]
        config['http'].append(('server', serv_info))
    return format_config(config) 
    


if __name__ == '__main__':
    print(gen_config(get_list(sys.argv[1])))
