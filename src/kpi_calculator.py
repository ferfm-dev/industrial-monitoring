"""
Calculates Industrial KPIs (OEE, MTBF, MTTR).
Feature: Transform data in metrics
"""

from sqlalchemy import func
from database import MachineEvent, Machine

def calculate_oee(session, machine_id=None, start_date=None, end_date=None):
    """
    OEE (Overall Equipament Effectiveness)
    OEE = AVAILABILITY * PERFORMANCE * QUALITY
    """

    query = session.query(MachineEvent).join(Machine)

    if machine_id:
        query = query.filter(Machine.machine_id == machine_id)
    if start_date:
        query = query.filter(MachineEvent.timestamp >= start_date)
    if end_date:
        query = query.filter(MachineEvent.timestamp <= end_date)
    
    events = query.all()

    if not events:
        return None
    
    total_time = sum(e.duration_minutes for e in events)
    downtime = sum(e.duration_minutes for e in events if e.event_type == 'downtime')
    production_time = total_time - downtime

    total_produced = sum(e.pieces_produced for e in events)
    total_defective = sum(e.pieces_defective for e in events)
    good_pieces = total_produced - total_defective

    machine = events[0].machine
    theoretical_production = (production_time / 60) * machine.production_rate

    availability = production_time / total_time if total_time > 0 else 0
    performance = total_produced / theoretical_production if theoretical_production > 0 else 0
    quality = good_pieces / total_produced if total_produced > 0 else 0

    oee = availability * performance * quality

    return {
        'oee': round(oee * 100, 2),
        'availability': round(availability * 100, 2),
        'performance': round(performance * 100, 2),
        'quality': round(quality * 100, 2),
        'total_produced': total_produced,
        'good_pieces': good_pieces,
        'downtime_minutes': downtime
    }

def calculate_mtbg_mttr(session, machine_id):
    """
    Calculates MTBF and MTTR
    """

    downtimes = session.query(MachineEvent).filter(
        MachineEvent.machine_id == machine_id,
        MachineEvent.event_type == 'downtime'
    ).order_by(MachineEvent.timestamp).all()

    if len(downtimes) < 2:
        return None
    
    # MTTR
    mttr = sum(d.duration_minutes for d in downtimes) / len(downtimes)

    # MTBF
    total_production_time = session.query(
        func.sum(MachineEvent.duration_minutes)
    ).filter(
        MachineEvent.machine_id == machine_id,
        MachineEvent.event_type == 'production'
    ).scalar() or 0

    mtbf = total_production_time / len(downtimes) if len(downtimes) > 0 else 0

    return {
        'mtbf_hours': round(mtbf / 60, 2),
        'mttr_hours': round(mttr / 60, 2),
        'num_failures': len(downtimes)
    }