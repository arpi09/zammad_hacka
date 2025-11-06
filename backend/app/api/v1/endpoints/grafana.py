"""
Grafana-compatible API endpoints.
Follows Single Responsibility Principle - handles only Grafana-specific endpoints.
"""
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.dependencies import get_zammad_service
from app.services.zammad_service import ZammadService

router = APIRouter()


@router.get("/tickets/timeseries")
async def get_tickets_timeseries(
    from_time: Optional[str] = Query(None, alias="from"),
    to_time: Optional[str] = Query(None, alias="to"),
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Get tickets as time-series data for Grafana.
    Returns data in Grafana's expected format.
    """
    try:
        tickets = await service.get_all_tickets()
        
        # Group tickets by creation date
        timeseries_data = {}
        
        for ticket in tickets:
            if ticket.created_at:
                # Parse date and group by day
                if isinstance(ticket.created_at, str):
                    date_obj = datetime.fromisoformat(ticket.created_at.replace("Z", "+00:00"))
                else:
                    date_obj = ticket.created_at
                
                date_key = date_obj.strftime("%Y-%m-%d")
                
                if date_key not in timeseries_data:
                    timeseries_data[date_key] = {
                        "time": int(date_obj.timestamp() * 1000),  # Grafana expects milliseconds
                        "value": 0,
                    }
                timeseries_data[date_key]["value"] += 1
        
        # Convert to Grafana format: [{"target": "series_name", "datapoints": [[value, timestamp], ...]}]
        result = []
        if timeseries_data:
            datapoints = sorted(
                [[data["value"], data["time"]] for data in timeseries_data.values()],
                key=lambda x: x[1]
            )
            result.append({
                "target": "Tickets Created",
                "datapoints": datapoints
            })
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating time-series data: {str(e)}"
        )


@router.get("/tickets/by-state")
async def get_tickets_by_state_grafana(
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Get ticket statistics by state in Grafana-compatible format.
    Returns data suitable for pie charts or bar charts.
    """
    try:
        statistics = await service.get_ticket_statistics()
        
        # Convert to Grafana table format
        result = []
        for state, count in statistics.tickets_by_state.items():
            result.append({
                "state": state,
                "count": count
            })
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting tickets by state: {str(e)}"
        )


@router.get("/tickets/by-priority")
async def get_tickets_by_priority_grafana(
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Get ticket statistics by priority in Grafana-compatible format.
    Returns data suitable for pie charts or bar charts.
    """
    try:
        statistics = await service.get_ticket_statistics()
        
        # Convert to Grafana table format
        result = []
        for priority, count in statistics.tickets_by_priority.items():
            result.append({
                "priority": priority,
                "count": count
            })
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting tickets by priority: {str(e)}"
        )


@router.get("/query")
async def grafana_query_endpoint(
    target: Optional[str] = Query(None),
    from_time: Optional[str] = Query(None, alias="from"),
    to_time: Optional[str] = Query(None, alias="to"),
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Generic Grafana query endpoint that supports multiple targets.
    This allows Grafana to query different metrics.
    """
    try:
        if target == "tickets_timeseries" or not target:
            return await get_tickets_timeseries(from_time, to_time, service)
        elif target == "tickets_by_state":
            return await get_tickets_by_state_grafana(service)
        elif target == "tickets_by_priority":
            return await get_tickets_by_priority_grafana(service)
        else:
            return []
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing Grafana query: {str(e)}"
        )


@router.get("/search")
async def grafana_search_endpoint():
    """
    Grafana search endpoint - returns available metrics/targets.
    """
    return [
        "tickets_timeseries",
        "tickets_by_state",
        "tickets_by_priority",
        "total_tickets",
        "open_tickets",
        "closed_tickets"
    ]


@router.get("/annotations")
async def grafana_annotations_endpoint():
    """
    Grafana annotations endpoint - for adding annotations to dashboards.
    """
    return []

