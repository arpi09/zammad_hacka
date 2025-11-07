"""
Native Grafana API endpoints (POST-based query API).
Works with Grafana's built-in JSON API datasource.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.v1.dependencies import get_zammad_service
from app.services.zammad_service import ZammadService

router = APIRouter()


@router.post("/query")
async def grafana_native_query(
    request: Request,
    service: ZammadService = Depends(get_zammad_service),
):
    """
    Native Grafana query endpoint (POST).
    Accepts Grafana's query format and returns data in expected format.
    """
    try:
        body = await request.json()
        targets = body.get("targets", [])
        
        results = []
        
        for target in targets:
            target_ref = target.get("target", target.get("refId", "A"))
            target_type = target.get("type", "timeseries")
            
            if target_ref == "tickets_timeseries" or "timeseries" in target_ref.lower():
                # Get time series data
                tickets = await service.get_all_tickets(fetch_all=True)
                
                # Group by time
                timeseries_data: Dict[str, int] = {}
                for ticket in tickets:
                    if ticket.created_at:
                        if isinstance(ticket.created_at, str):
                            date_obj = datetime.fromisoformat(ticket.created_at.replace("Z", "+00:00"))
                        else:
                            date_obj = ticket.created_at
                        
                        date_key = date_obj.strftime("%Y-%m-%d")
                        timeseries_data[date_key] = timeseries_data.get(date_key, 0) + 1
                
                # Convert to Grafana format
                datapoints = []
                for date_key, count in sorted(timeseries_data.items()):
                    date_obj = datetime.strptime(date_key, "%Y-%m-%d")
                    timestamp_ms = int(date_obj.timestamp() * 1000)
                    datapoints.append([count, timestamp_ms])
                
                results.append({
                    "target": "Tickets Created",
                    "datapoints": datapoints
                })
            
            elif target_ref == "tickets_by_state" or "state" in target_ref.lower():
                stats = await service.get_ticket_statistics()
                
                # Convert to table format
                table_data = {
                    "columns": [
                        {"text": "State", "type": "string"},
                        {"text": "Count", "type": "number"}
                    ],
                    "rows": [[state, count] for state, count in stats.tickets_by_state.items()],
                    "type": "table"
                }
                
                results.append({
                    "target": "Tickets by State",
                    "datapoints": [],
                    "table": table_data
                })
            
            elif target_ref == "tickets_by_priority" or "priority" in target_ref.lower():
                stats = await service.get_ticket_statistics()
                
                table_data = {
                    "columns": [
                        {"text": "Priority", "type": "string"},
                        {"text": "Count", "type": "number"}
                    ],
                    "rows": [[priority, count] for priority, count in stats.tickets_by_priority.items()],
                    "type": "table"
                }
                
                results.append({
                    "target": "Tickets by Priority",
                    "datapoints": [],
                    "table": table_data
                })
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing query: {str(e)}"
        )


@router.get("/")
async def grafana_native_root():
    """Root endpoint for Grafana native API."""
    return {
        "message": "Grafana Native API",
        "version": "1.0.0",
        "endpoints": {
            "query": "POST /query - Query endpoint",
            "search": "GET /search - Search available metrics"
        }
    }

