from os import getenv

from flask import Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, CollectorRegistry, Counter, generate_latest, multiprocess

request_counter = Counter(
    name="request_by_template",
    documentation="Total requests received by name of the returned template.",
    labelnames=("template",),
    namespace="lethe",
)


def handle_metrics() -> Response:
    registry = REGISTRY

    if getenv("PROMETHEUS_MULTIPROC_DIR"):
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)

    headers = {"Content-Type": CONTENT_TYPE_LATEST}
    return Response(generate_latest(registry), status=200, headers=headers)
