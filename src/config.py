host = {
    'environment' = os.getenv('ENV', 'Undefined')
}

database = {
    'host' = os.getenv('TSDB_HOST', ''),
    'port' = os.getenv('TSDB_PORT', ''),
    'database' = os.getenv('TSDB_DB', ''),
    'username' = os.getenv('TSDB_USER', ''),
    'password' = os.getenv('TSDB_PASSWD', ''),
}