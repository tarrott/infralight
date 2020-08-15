# Changelog

- [Changelog](#changelog)
  - [0.2.0](#020)
  - [0.1.0](#010)

## 0.2.0
- Add new feature X
- Add new feature Y

## 0.1.0

- First implementation of the Alenza Core Helm Chart
  - Add Kafka support by using Strimzi. This adds support for the creation of:
    - Kafka Brokers
    - Kafka Connect clusters
  - Add support for Schema Registry (not handled by Strimzi, since it doesn't support it)
  - Add MySQL through `Presslabs` helm chart