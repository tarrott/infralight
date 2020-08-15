# DevOps-Monitoring

### Docker Host Exporter


### TimescaleDB

Connect to CLI tool `psql` using: `docker exec -it timescaledb -U postgres`

### Grafana


### Release Manager


### Deployments
###### .env config file
The `docker-host-exporter` and the `release-manager` require database credentials to read & write data to `timescaledb`.

###### Monitoring Stack (Central Host)
Only one node will have the entire monitoring stack deployed to it:
`docker-compose up -d --build`

###### Additional Hosts
All additional nodes will only require the `docker-host-exporter` service to be deployed:
`docker-compose up -d --build docker-host-exporter`