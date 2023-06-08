from abc import ABCMeta, abstractmethod

from claranet.entities import Customer, Ticket


class CounterInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name: str, max_queue_capacity: int, time_to_process_each_ticket: int):
        """Initializer for the class Counter.

        Args:
            name (str): Name of the counter.
            max_queue_capacity (int): Maximum queue for the counter.
            time_to_process_each_ticket (int): Time required to process each time at the counter.
        """

    @abstractmethod
    def issue_ticket(self, customer: Customer) -> Ticket:
        """Issues a ticket to the customer.

        Args:
            customer (Customer): Customer object to which ticket should be issued.

        Returns:
            Ticket: Issued ticket.

        """


class TicketBookingCenterInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, max_counters: int, max_queue_capacity: int, time_to_process_each_ticket: int) -> None:
        """Initializer for the class TicketBookingCenter.

        Args:
            max_counters (int): Maximum number of counters available at the Booking center.
            max_queue_capacity (int): Maximum queue for the counter.
            time_to_process_each_ticket (int): Time required to process each time at the counter.
        """

    @abstractmethod
    def orchestrate(self, customers: list[Customer]) -> list[Customer]:
        """Orchestrate the usage and issuance of tickets by the Counter.

        Args:
            customers (list[Customer]): List of customers would be available.

        Returns:
            list[Customer]: List of customers issued with tickets.

        """
