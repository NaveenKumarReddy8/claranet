"""Ticket booking Center module."""

from datetime import timedelta
from logging import DEBUG, FileHandler, Formatter, Logger, getLogger
from queue import Queue

from claranet.constants import data
from claranet.entities import Customer, Ticket
from claranet.interfaces import CounterInterface, TicketBookingCenterInterface

# logger setup.
logger: Logger = getLogger("claranet-ticket-booking-system")
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = FileHandler(filename="claranet_ticket_booking_system_logs.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(level=DEBUG)
logger.addHandler(file_handler)
logger.setLevel(level=DEBUG)


class Counter(CounterInterface):
    """Counter class to deal with methods of billing counter."""

    def __init__(self, name: str, max_queue_capacity: int, time_to_process_each_ticket: int):
        """Initializer for the class Counter.

        Args:
            name (str): Name of the counter.
            max_queue_capacity (int): Maximum queue for the counter.
            time_to_process_each_ticket (int): Time required to process each time at the counter.
        """
        self.name = name
        self.queue = Queue(maxsize=max_queue_capacity)
        self.time_to_process_each_ticket = time_to_process_each_ticket
        self.previously_issued_time = None

    def issue_ticket(self, customer: Customer) -> Ticket:
        """Issues a ticket to the customer.

        Args:
            customer (Customer): Customer object to which ticket should be issued.

        Returns:
            Ticket: Issued ticket.

        """
        self.queue.put("customer")
        logger.debug("called a put method of queue.")
        if self.previously_issued_time is None:
            issued_time = customer.entered_time + timedelta(
                seconds=self.queue.qsize() * self.time_to_process_each_ticket
            )
            self.previously_issued_time = issued_time
        else:
            issued_time = max(self.previously_issued_time, customer.entered_time) + timedelta(
                seconds=time_to_process_each_ticket
            )
            self.previously_issued_time = issued_time
        logger.info("Returning the ticket.")
        return Ticket(issued_at_counter=self.name, issue_time=issued_time)

    def __repr__(self):
        """Overridden __repr__ method."""
        return f"Counter {self.name}"


class TicketBookingCenter(TicketBookingCenterInterface):
    def __init__(self, max_counters: int, max_queue_capacity: int, time_to_process_each_ticket: int) -> None:
        """Initializer for the class TicketBookingCenter.

        Args:
            max_counters (int): Maximum number of counters available at the Booking center.
            max_queue_capacity (int): Maximum queue for the counter.
            time_to_process_each_ticket (int): Time required to process each time at the counter.
        """
        self.max_counters = max_counters
        self.counters = [
            Counter(
                name=f"C{num}",
                max_queue_capacity=max_queue_capacity,
                time_to_process_each_ticket=time_to_process_each_ticket,
            )
            for num in range(1, max_counters + 1)
        ]
        self.max_queue_capacity = max_queue_capacity
        self.time_to_process_each_ticket = time_to_process_each_ticket
        self.in_process = Queue(maxsize=1)

    def orchestrate(self, customers: list[Customer]) -> list[Customer]:
        """Orchestrate the usage and issuance of tickets by the Counter.

        Args:
            customers (list[Customer]): List of customers would be available.

        Returns:
            list[Customer]: List of customers issued with tickets.

        """
        while True:
            if all([c.number_of_tickets == len(c.tickets) for c in customers]):
                logger.info("All the customers have successfully received tickets.")
                break
            for index, customer in enumerate(customers):
                if customer.number_of_tickets == len(customer.tickets):
                    continue
                for counter in self.counters:
                    if counter.queue.full():
                        continue
                    ticket: Ticket = counter.issue_ticket(customer=customer)
                    customer.tickets.append(ticket)
                    print(f"{counter.name} issued the ticket for {customer.name}: {ticket}")
                    if counter.previously_issued_time < customers[index - 1].entered_time:
                        counter.queue.get()
                    break

        return customers


def get_customer_data() -> list[Customer]:
    """Get customer data.

    Returns:
        list[Customer]: List of Customer class objects given as input.
    """
    return [Customer(**customer_data) for customer_data in data]


if __name__ == "__main__":
    max_counters = int(input("Please enter the maximum number of counters for this booking center: \t").strip())
    max_queue_capacity = int(input("Please enter the maximum queue capacity for a counter: \t").strip())
    time_to_process_each_ticket = int(
        input("Please enter the time taken to process each ticket in seconds: \t").strip()
    )
    print("*" * 60)
    ticket_booking_center = TicketBookingCenter(
        max_counters=max_counters,
        max_queue_capacity=max_queue_capacity,
        time_to_process_each_ticket=time_to_process_each_ticket,
    )
    customers = ticket_booking_center.orchestrate(get_customer_data())
    print("*" * 60)
    for c in customers:
        print(
            f"Total time consumed by {c.name} who entered the booking center at: {c.entered_time} for {c.number_of_tickets} tickets is {c.tickets[-1].issue_time-c.entered_time}"
        )
