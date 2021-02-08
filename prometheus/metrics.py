from prometheus_client import Counter, CollectorRegistry

registry = CollectorRegistry()

# prometheus will add _total at the end of the metric name if its a Counter
# so this metric full name will be lethe_requests_by_status_total
request_counter = Counter(
    name="requests_by_status",
    documentation="Total requests received by response's status code.",
    labelnames=("status_code",),
    namespace="lethe"
)
