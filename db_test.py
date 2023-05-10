from datetime import datetime

from component_management_system.models import Person

p1 = Person(
    id=23,
    lname="John",
    fname="Chris",
    timestamp=datetime.now(),
)
