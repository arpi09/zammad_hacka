"""
Prometheus-compatible endpoints for Grafana.
Prometheus is a built-in Grafana datasource - no plugins needed!
"""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import Response
from pydantic import BaseModel

from app.api.v1.dependencies import get_zammad_service
from app.services.zammad_service import ZammadService

router = APIRouter()


class PrometheusQuery(BaseModel):
    """Prometheus query request model."""
    query: str
    time: str = None
    timeout: str = "30s"


@router.get("/")
async def prometheus_root():
    """
    Prometheus API root endpoint.
    Returns API information.
    """
    return {
        "status": "success",
        "data": {
            "version": "1.0.0",
            "endpoints": {
                "metrics": "/api/v1/prometheus/metrics",
                "query": "/api/v1/prometheus/api/v1/query",
                "label_values": "/api/v1/prometheus/api/v1/label/__name__/values"
            }
        }
    }


@router.get("/metrics")
async def prometheus_metrics(
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Prometheus metrics endpoint.
    Returns data in Prometheus exposition format (plain text).
    """
    try:
        statistics = await service.get_ticket_statistics()
        
        # Format as Prometheus metrics
        metrics = []
        
        # Counter metrics
        metrics.append(f"zammad_tickets_total {statistics.total_tickets}")
        metrics.append(f"zammad_tickets_open {statistics.open_tickets}")
        metrics.append(f"zammad_tickets_closed {statistics.closed_tickets}")
        
        # Tickets by state
        for state, count in statistics.tickets_by_state.items():
            state_label = state.replace(" ", "_").lower()
            metrics.append(f'zammad_tickets_by_state{{state="{state}"}} {count}')
        
        # Tickets by priority
        for priority, count in statistics.tickets_by_priority.items():
            priority_label = priority.replace(" ", "_").lower()
            metrics.append(f'zammad_tickets_by_priority{{priority="{priority}"}} {count}')
        
        # Return as plain text (Prometheus format)
        return Response(content="\n".join(metrics), media_type="text/plain")
    
    except Exception as e:
        return Response(content=f"# Error: {str(e)}\n", media_type="text/plain")


@router.get("/api/v1/query")
@router.post("/api/v1/query")
async def prometheus_query_api(
    request: Request,
    query: str = Query(None, description="PromQL query"),
    time: str = Query(None, description="Evaluation timestamp"),
    timeout: str = Query("30s", description="Query timeout"),
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Prometheus query API endpoint.
    Supports both GET and POST requests (Grafana uses POST).
    Supports basic PromQL queries.
    """
    try:
        # Handle POST request body
        if request.method == "POST":
            try:
                body = await request.json()
                query = body.get("query") or query
                time = body.get("time") or time
                timeout = body.get("timeout") or timeout
            except:
                # If JSON parsing fails, use query params
                pass
        
        # If no query provided, return empty result (Grafana sometimes tests with empty query)
        if not query:
            return {
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": []
                }
            }
        
        statistics = await service.get_ticket_statistics()
        
        # Parse query and build results
        results = []
        
        if "zammad_tickets_total" in query:
            results.append({
                "metric": {"__name__": "zammad_tickets_total"},
                "value": [int(datetime.now().timestamp()), str(statistics.total_tickets)]
            })
        
        if "zammad_tickets_open" in query:
            results.append({
                "metric": {"__name__": "zammad_tickets_open"},
                "value": [int(datetime.now().timestamp()), str(statistics.open_tickets)]
            })
        
        if "zammad_tickets_closed" in query:
            results.append({
                "metric": {"__name__": "zammad_tickets_closed"},
                "value": [int(datetime.now().timestamp()), str(statistics.closed_tickets)]
            })
        
        # Handle tickets_by_state queries
        if "zammad_tickets_by_state" in query:
            for state, count in statistics.tickets_by_state.items():
                results.append({
                    "metric": {
                        "__name__": "zammad_tickets_by_state",
                        "state": state
                    },
                    "value": [int(datetime.now().timestamp()), str(count)]
                })
        
        # Handle tickets_by_priority queries
        if "zammad_tickets_by_priority" in query:
            for priority, count in statistics.tickets_by_priority.items():
                results.append({
                    "metric": {
                        "__name__": "zammad_tickets_by_priority",
                        "priority": priority
                    },
                    "value": [int(datetime.now().timestamp()), str(count)]
                })
        
        # If no specific match, try to return total
        if not results:
            results.append({
                "metric": {"__name__": query.split("{")[0] if "{" in query else query},
                "value": [int(datetime.now().timestamp()), "0"]
            })
        
        # Return Prometheus query result format
        return {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": results
            }
        }
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return {
            "status": "error",
            "errorType": "internal_error",
            "error": str(e),
            "detail": error_detail
        }


@router.get("/api/v1/query_range")
@router.post("/api/v1/query_range")
async def prometheus_query_range(
    request: Request,
    query: str = Query(None, description="PromQL query"),
    start: str = Query(None, description="Start timestamp"),
    end: str = Query(None, description="End timestamp"),
    step: str = Query("15s", description="Query resolution step width"),
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Prometheus query_range API endpoint for time-series queries.
    Grafana uses this for graph visualizations.
    """
    try:
        # Handle POST request body
        if request.method == "POST":
            try:
                body = await request.json()
                query = body.get("query") or query
                start = body.get("start") or start
                end = body.get("end") or end
                step = body.get("step") or step
            except:
                pass
        
        if not query:
            return {
                "status": "success",
                "data": {
                    "resultType": "matrix",
                    "result": []
                }
            }
        
        statistics = await service.get_ticket_statistics()
        
        # Parse time range
        start_time = int(start) if start else int(datetime.now().timestamp()) - 3600
        end_time = int(end) if end else int(datetime.now().timestamp())
        
        # Parse step (e.g., "15s", "1m", "1h")
        step_seconds = 15  # default
        if step:
            if step.endswith("s"):
                step_seconds = int(step[:-1])
            elif step.endswith("m"):
                step_seconds = int(step[:-1]) * 60
            elif step.endswith("h"):
                step_seconds = int(step[:-1]) * 3600
        
        # Generate time series data points across the range
        # Since we don't have historical data, return the same value for all points
        def generate_time_series(value):
            values = []
            current = start_time
            while current <= end_time:
                values.append([current, str(value)])
                current += step_seconds
            return values
        
        results = []
        
        if "zammad_tickets_total" in query:
            results.append({
                "metric": {"__name__": "zammad_tickets_total"},
                "values": generate_time_series(statistics.total_tickets)
            })
        
        if "zammad_tickets_open" in query:
            results.append({
                "metric": {"__name__": "zammad_tickets_open"},
                "values": generate_time_series(statistics.open_tickets)
            })
        
        if "zammad_tickets_closed" in query:
            results.append({
                "metric": {"__name__": "zammad_tickets_closed"},
                "values": generate_time_series(statistics.closed_tickets)
            })
        
        if "zammad_tickets_by_state" in query:
            for state, count in statistics.tickets_by_state.items():
                results.append({
                    "metric": {
                        "__name__": "zammad_tickets_by_state",
                        "state": state
                    },
                    "values": generate_time_series(count)
                })
        
        if "zammad_tickets_by_priority" in query:
            for priority, count in statistics.tickets_by_priority.items():
                results.append({
                    "metric": {
                        "__name__": "zammad_tickets_by_priority",
                        "priority": priority
                    },
                    "values": generate_time_series(count)
                })
        
        if not results:
            results.append({
                "metric": {"__name__": query.split("{")[0] if "{" in query else query},
                "values": generate_time_series(0)
            })
        
        return {
            "status": "success",
            "data": {
                "resultType": "matrix",
                "result": results
            }
        }
    
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "errorType": "internal_error",
            "error": str(e)
        }


@router.get("/api/v1/label/__name__/values")
async def prometheus_label_values():
    """
    Prometheus label values endpoint.
    Returns available metric names.
    """
    return {
        "status": "success",
        "data": [
            "zammad_tickets_total",
            "zammad_tickets_open",
            "zammad_tickets_closed",
            "zammad_tickets_by_state",
            "zammad_tickets_by_priority"
        ]
    }


@router.get("/api/v1/label/{label_name}/values")
async def prometheus_label_values_specific(label_name: str):
    """
    Prometheus label values for specific label.
    """
    if label_name == "state":
        return {
            "status": "success",
            "data": ["open", "closed", "pending", "merged"]
        }
    elif label_name == "priority":
        return {
            "status": "success",
            "data": ["low", "normal", "high", "critical"]
        }
    else:
        return {
            "status": "success",
            "data": []
        }

