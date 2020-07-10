import datetime
import os
import platform
import time

import distro
import docker
import psutil
import psycopg2

import config


def get_host_details():
    host_details = {}
    uptime_seconds = time.time() - psutil.boot_time()
    host_details['uptime'] = str(datetime.timedelta(seconds=uptime_seconds))
    host_details['total_cpu'] = psutil.cpu_count()
    host_details['total_memory'] = str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)) + ' GiB'
    host_details['os'] = platform.system()
    host_details['environment'] = config.host['environment']
    if host_details['os'] == 'Linux':
        host_details['os'] = distro.linux_distribution(full_distribution_name=False)
    elif host_details['os'] == 'Windows':
        host_details['os'] += ' ' + platform.release()
    return host_details


def get_resource_usage():
    resource_usage = {}
    resource_usage['cpu_usage'] = psutil.cpu_percent(interval=1)
    resource_usage['memory_usage'] = psutil.virtual_memory().percent
    return resource_usage


def get_paths():
    paths = os.getenv('DISK_PATHS', '/')
    paths = paths.split(",")
    return paths


def get_disk_usage(paths):
    disk_usage = {}
    for path in paths:
        disk_usage[path] = psutil.disk_usage(path).percent
    return disk_usage


def get_docker_host_details(docker_host, host_details):
    system_info = docker_host.info()
    host_details['os'] = system_info['OperatingSystem']
    host_details['containers_running'] = system_info['ContainersRunning']
    host_details['containers_stopped'] = system_info['ContainersStopped']
    host_details['docker_cpus'] = system_info['NCPU']
    host_details['docker_memory'] = str(round(float(system_info['MemTotal']) / (1024 * 1024 * 1024), 2)) + ' GiB'
    return host_details


def get_container_details(docker_host):
    container_data = {}
    containers = docker_host.df()['Containers']
    for container in containers:
        details = {}
        name = container['Names'][0]
        image = container['Image']
        if image.startswith('sha256'):
            image = 'untagged'
        details['image'] = image
        details['state'] = container['State']
        details['status'] = container['Status']
        details['mounts'] = len(container['Mounts'])
        details['networks'] = ','.join(list(container['NetworkSettings']['Networks'].keys()))
        container_data[name] = details
    return container_data


def update_database():
    try:
        connection = psycopg2.connect(host = config.database['host'],
                                      port = config.database['port'],
                                      database = config.database['database'],
                                      user = config.database['username'],
                                      password= = config.database['password'])
    except psycopg2.OperationalError:
        print('Could not connect to {}'.format(config.database['host']))

    cursor = connection.cursor()


def main():
    host_details = get_host_details()
    print(host_details)
    resource_usage = get_resource_usage()
    print(resource_usage)
    paths = get_paths()
    disk_usage = get_disk_usage(paths)
    print(disk_usage)

    if os.environ.get('DOCKER') != None:
        docker_host = docker.from_env()
        host_details = get_docker_host_details(docker_host, host_details)
        print(host_details)
        container_data = get_container_details(docker_host)
        print(container_data)

    update_database()


if __name__=='__main__':
    main()