from prometheus_client import Counter, CollectorRegistry

registry = CollectorRegistry()

# prometheus will add _total at the end of the metric name if its a Counter
# so this metric full name will be lethe_request_by_template_total
request_counter = Counter(
    name="request_by_template",
    documentation="Total requests received by name of the returned template.",
    labelnames=("template",),
    namespace="lethe",
)
