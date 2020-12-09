## envoy edge proxy, OTel Collector OTLP/grpc termination example

This is a [spin-off](https://github.com/diorahman/hello-envoy-grpc-tls) for testing envoy with OTel Collector doing TLS termination.

```
$ docker compose up
$ cd client && python main.py
```

This example defaults to run on `localhost`. Adjust accordingly.

To generate a new cert/key, just run the `./create-cert.sh`

Note: The client patches a gRPC option in order to have Envoy accept
self signed certificates, while still doing TLS handling & termination.
