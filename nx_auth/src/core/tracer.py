from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)


def configure_tracer(config: dict) -> None:
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({"service.name": "auth-service"}))
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                collector_endpoint="http://{host}:{port}/api/traces".format(**config),
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
