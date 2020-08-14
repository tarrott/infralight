import os

host = {
    'name': os.getenv('HOSTNAME'),
    'environment': os.getenv('ENV'),
    'disk_paths': os.getenv('DISK_PATHS', '/'),
    'docker': os.getenv('DOCKER', None)
}

database = {
    'host': os.getenv('TSDB_HOST', 'timescaledb'),
    'port': os.getenv('TSDB_PORT', '5432'),
    'database': os.getenv('TSDB_DB', 'postgres'),
    'username': os.getenv('TSDB_USER', 'postgres'),
    'password': os.getenv('TSDB_PASSWD', 'password')
}