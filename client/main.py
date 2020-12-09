from opentelemetry import trace
from opentelemetry.exporter.otlp.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from grpc import ssl_channel_credentials
import grpc

# Patch grpc.secure_channel() in order to have it accept
# self-signed certificates.
grpc.secure_channel.__defaults__ = (
        (
            ('grpc.ssl_target_name_override', 'hello.com',),
            ('grpc.default_authority', 'hello.com',),
        ),
        None)

with open('../envoy/pem/crt', 'rb') as f:
    trusted_certs = f.read()

exporter = OTLPSpanExporter(
    endpoint="127.0.0.1:10000",
    insecure=False,
    credentials=ssl_channel_credentials(root_certificates=trusted_certs),
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchExportSpanProcessor(exporter)

trace.get_tracer_provider().add_span_processor(span_processor)
with tracer.start_as_current_span("foo"):
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello world from OpenTelemetry Python!")
