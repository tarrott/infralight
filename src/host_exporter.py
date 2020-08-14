import datetime
import platform
import sys
import time

import distro
import docker
import psutil
import psycopg2

import config


def get_host_details():
    host_details = {}
    uptime_seconds = time.time() - psutil.boot_time()
    host_details['uptime'] = str(datetime.timedelta(seconds=uptime_seconds).days) + ' days'
    
    host_details['total_cpu'] = str(psutil.cpu_count()) + ' CPUs'
    host_details['total_memory'] = str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)) + ' GiB'
    
    host_details['hostname'] = config.host['name']
    host_details['os'] = platform.system()
    host_details['environment'] = config.host['environment']
    if host_details['os'] == 'Linux':
        host_details['os'] = distro.linux_distribution(full_distribution_name=False)
    elif host_details['os'] == 'Windows':
        host_details['os'] += ' ' + platform.release()
    
    return host_details


def get_resource_usage():
    resource_usage = {}
    resource_usage['cpu_usage'] = psutil.cpu_percent(interval=2)
    resource_usage['memory_usage'] = psutil.virtual_memory().percent
    return resource_usage


def get_paths():
    paths = config.host['disk_paths']
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
    host_details['containers_running'] = system_info['ContainersRunning'] - 1
    host_details['containers_stopped'] = system_info['ContainersStopped']
    return host_details


def get_container_details(docker_host):
    container_data = {}
    containers = docker_host.df()['Containers']
    for container in containers:
        details = {}
        name = container['Names'][0]
        if container['Names'][0] == '/host-exporter':
            continue
        if name[0] == '/':
            name = name[1:]

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


def update_database(host_details, resource_usage, disk_usage, container_data):
    connection = False
    try:
        connection = psycopg2.connect(host = config.database['host'],
                                      port = config.database['port'],
                                      database = config.database['database'],
                                      user = config.database['username'],
                                      password = config.database['password'])
        cursor = connection.cursor()
        host_insert = 'INSERT INTO monitoring.hosts (time, hostname, environment, os, uptime, total_cpu, total_memory, cpu_usage, memory_usage, disk_usage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        host_values = ('NOW()', host_details['hostname'], host_details['environment'], host_details['os'], host_details['uptime'], host_details['total_cpu'], host_details['total_memory'], resource_usage['cpu_usage'], resource_usage['memory_usage'], disk_usage['/'])
        
        if container_data:
            host_insert = 'INSERT INTO monitoring.hosts (time, hostname, environment, os, uptime, total_cpu, total_memory, cpu_usage, memory_usage, disk_usage, containers_running, containers_stopped) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            host_values = ('NOW()', host_details['hostname'], host_details['environment'], host_details['os'], host_details['uptime'], host_details['total_cpu'], host_details['total_memory'], resource_usage['cpu_usage'], resource_usage['memory_usage'], disk_usage['/'], host_details['containers_running'], host_details['containers_stopped'])

            for container in container_data:
                container_insert = 'INSERT INTO monitoring.containers (time, name, image, state, status, mounts, networks) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                container_values = ('NOW()', container, container_data[container]['image'], container_data[container]['state'], container_data[container]['status'], container_data[container]['mounts'], container_data[container]['networks'])
                cursor.execute(container_insert, container_values)

        cursor.execute(host_insert, host_values)
        connection.commit()
        print("Record inserted successfully into monitoring table")
    except (Exception, psycopg2.Error) as error:
        print(f'Failed to insert record.', error)
        sys.exit(1)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def main():
    host_details = get_host_details()
    resource_usage = get_resource_usage()
    paths = get_paths()
    disk_usage = get_disk_usage(paths)

    container_data = {}
    if config.host['docker'] != None:
        docker_host = docker.from_env()
        host_details = get_docker_host_details(docker_host, host_details)
        container_data = get_container_details(docker_host)

    update_database(host_details, resource_usage, disk_usage, container_data)


if __name__=='__main__':
    main()