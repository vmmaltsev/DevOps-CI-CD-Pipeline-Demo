# Monitoring System Documentation

This document describes the monitoring system implemented in this project, including Prometheus, Grafana, and Alertmanager.

## Overview

The monitoring system provides real-time visibility into application health, performance metrics, and alerts for potential issues. The system consists of:

- **Prometheus**: Time-series database for metrics collection and storage
- **Grafana**: Visualization platform for metrics and dashboards
- **Alertmanager**: Alert handling and notification system

## Architecture

The monitoring architecture follows a typical Prometheus deployment pattern:

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│            │      │            │      │            │
│ Flask App  │─────▶│ Prometheus │─────▶│  Grafana   │
│            │      │            │      │            │
└────────────┘      └──────┬─────┘      └────────────┘
                          │
                          ▼
                    ┌────────────┐
                    │            │
                    │Alertmanager│
                    │            │
                    └────────────┘
```

- The Flask application exposes metrics via the `/metrics` endpoint
- Prometheus scrapes metrics from the application at regular intervals
- Grafana visualizes the metrics collected by Prometheus
- Alertmanager handles alert notifications based on Prometheus rules

## Metrics Collection

### Application Metrics

The Flask application exposes the following metrics:

- **HTTP Request Counts**: Total number of HTTP requests by endpoint
- **Request Duration**: Histogram of request processing times
- **Status Codes**: Count of responses by status code
- **Application Info**: Metadata about the application version

These metrics are exposed via the `/metrics` endpoint and are automatically collected by Prometheus.

### System Metrics

In addition to application metrics, the following system metrics can be monitored:

- CPU usage
- Memory usage
- Disk I/O
- Network traffic

## Prometheus Configuration

Prometheus is configured via `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'flask-app'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['web:8080']

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

This configuration:
- Sets a global scrape interval of 15 seconds
- Collects metrics from the Flask application at `web:8080/metrics`
- Monitors Prometheus itself

## Grafana Dashboards

Grafana is pre-configured with a dashboard for the Flask application:

- **Flask Application Dashboard**: Overview of application performance metrics

The dashboard includes:
- Request rate by endpoint
- Response time percentiles
- HTTP status code distribution
- Total request count

### Dashboard Configuration

Dashboards are configured in JSON format at `monitoring/grafana/dashboards/flask-dashboard.json`.

Grafana is provisioned with:

1. **Data Source**: Prometheus at `http://prometheus:9090`
2. **Dashboard**: Flask Application Dashboard

## Alerting System

Alerting is managed by Alertmanager, which is configured via `alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'job']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
  receiver: 'web.hook'

receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://example.com/alert'
    send_resolved: true
```

This configuration:
- Groups alerts by name and job
- Waits 30s before sending initial notifications
- Waits 5m before sending updates for changed alerts
- Repeats notifications every 12h for unresolved alerts
- Sends notifications to the configured webhook

## Default Alert Rules

The following alert rules can be configured in Prometheus:

1. **HighErrorRate**:
   - Triggers when the HTTP error rate exceeds 5%
   - Severity: warning

2. **ServiceDown**:
   - Triggers when the service is unreachable
   - Severity: critical

3. **HighResponseTime**:
   - Triggers when the 95th percentile response time exceeds 500ms
   - Severity: warning

## Accessing Monitoring Tools

After deployment, the monitoring tools are available at:

- **Prometheus**: http://hostname:9090
- **Grafana**: http://hostname:3000 (default credentials: admin/admin)
- **Alertmanager**: http://hostname:9093

## Extending the Monitoring System

### Adding New Metrics

To add new metrics to the application:

1. Add new metrics in the Flask application using the Prometheus client library:

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Counter example
request_count = metrics.counter(
    'request_count', 'Number of requests received',
    labels={'endpoint': lambda: request.endpoint}
)

# Gauge example
in_progress = metrics.gauge(
    'in_progress', 'Number of requests in progress',
    labels={'endpoint': lambda: request.endpoint}
)

# Histogram example
request_latency = metrics.histogram(
    'request_latency_seconds', 'Request latency in seconds',
    labels={'endpoint': lambda: request.endpoint}
)
```

2. Use the metrics in your code:

```python
@app.route('/example')
@request_count
@request_latency
def example():
    with in_progress.track_inprogress():
        # Your code here
        return "Example response"
```

### Adding New Dashboards

To add a new dashboard to Grafana:

1. Create a new dashboard in Grafana UI
2. Export the dashboard to JSON
3. Save the JSON to `monitoring/grafana/dashboards/`
4. Update the provisioning configuration if needed

### Configuring Alerts

To add new alert rules:

1. Create a new `alerts.yml` file:

```yaml
groups:
- name: application-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(flask_http_request_total{status=~"5.."}[5m]) / rate(flask_http_request_total[5m]) > 0.05
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "High error rate detected"
      description: "Error rate is above 5% (current value: {{ $value }})"
```

2. Add the rules file to Prometheus:

```yaml
rule_files:
  - "alerts.yml"
```

3. Configure notification channels in Alertmanager

## Best Practices

1. **Retention Policy**: Configure Prometheus retention based on available storage and monitoring needs
2. **Dashboard Organization**: Group related metrics in the same dashboard panels
3. **Alert Thresholds**: Set appropriate thresholds based on application behavior
4. **Notification Channels**: Configure multiple notification channels for critical alerts
5. **Regular Review**: Periodically review dashboards and alerts to ensure they remain relevant 