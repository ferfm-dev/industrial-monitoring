"""
Script to create database and fill it up with initial data.
RUN THIS SCRIT FIRST!!!!!!!!
"""

from datetime import datetime, timedelta
from src.database import get_engine, create_engine, create_tables, get_session, Machine, MachineEvent
from src.data_generator import generate_machines, generate_events_for_machine

def setup_database():
    engine = get_engine()
    create_tables(engine)

    session = get_session(engine)

    machines_data = generate_machines(5)

    for machine_data in machines_data:
        machine = Machine(**machine_data)
        session.add(machine)
    
    session.commit()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    machines = session.query(Machine).all()
    total_events = 0

    for machine in machines:
        machine_dict = {
            'id': machine.id,
            'type': machine.type,
            'production_rate': machine.production_rate
        }

        events = generate_events_for_machine(machine_dict, start_date, end_date)

        for event_data in events:
            event = MachineEvent(**event_data)
            session.add(event)
        
        total_events += len(events)
    
    session.commit()
    session.close()

if __name__ == '__main__':
    setup_database()