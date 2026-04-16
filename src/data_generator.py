"""
Generate mock data for the industries machines
Feature: Make prod/downtime events
"""

import random
from datetime import timedelta

MACHINE_TYPES = {
    'CNC': {'rate': 60, 'downtime_prob': 0.05},
    'Prensa': {'rate': 120, 'downtime_prob': 0.08},
    'Torno': {'rate': 40, 'downtime_prob': 0.03},
    'Injetora': {'rate': 200, 'downtime_prob': 0.10},
}

DOWNTIME_REASONS = [
    'Troca de ferramenta',
    'Falta de matéria-prima',
    'Manutenção preventiva',
    'Quebra inesperada',
    'Ajuste de qualidade',
    'Falta de operador',
]

def generate_machines(num_machines=5):
    machines = []

    for i in range(num_machines):
        machine_type = random.choice(list(MACHINE_TYPES.keys()))
        machines.append({
            'name': f'{machine_type}-{i+1:02d}',
            'type': machine_type,
            'production_rate': MACHINE_TYPES[machine_type]['rate']
        })
    return machines

def generate_events_for_machine(machine, start_date, end_date):
    events = []
    current_time = start_date

    while current_time < end_date:

        if random.random() < MACHINE_TYPES[machine['type']]['downtime_prob']:
            event = {
                'machine_id': machine['id'],
                'timestamp': current_time,
                'event_type': 'downtime',
                'duration_minutes': random.randint(15, 180),
                'pieces_produced': 0,
                'pieces_defective': 0,
                'downtime_reason': random.choice(DOWNTIME_REASONS)
            }
        else:
            duration = random.randint(30, 120)
            expected_pieces = int((machine['production_rate'] / 60) * duration)

            actual_pieces = int(expected_pieces * random.uniform(0.8, 1.05))

            defective = int(actual_pieces * random.uniform(0, 0.05))

            event = {
                'machine_id': machine['id'],
                'timestamp': current_time,
                'event_type': 'production',
                'duration_minutes': duration,
                'pieces_produced': actual_pieces,
                'pieces_defective': defective,
                'downtime_reason': None
            }

        events.append(event)
        current_time += timedelta(minutes=event['duration_minutes'])
    
    return events