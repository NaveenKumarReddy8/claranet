"""Entities/dataclasses module."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Ticket:
    issued_at_counter: None | str
    issue_time: datetime
    ticket_id: UUID = field(default_factory=uuid4)


@dataclass
class Customer:
    name: str
    entered_time: datetime
    number_of_tickets: int
    tickets: None | list = field(default_factory=list)

    def __post_init__(self):
        self.entered_time = datetime.strptime(self.entered_time, "%Y-%m-%d %H:%M:%S")
