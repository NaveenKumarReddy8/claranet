import datetime

from pytest import fixture
from pytest_mock import MockFixture

from claranet.entities import Customer, Ticket
from claranet.ticket_booking_center import Counter, TicketBookingCenter, get_customer_data


@fixture
def counter():  # This is pytest fixture object.
    return Counter("C1", 4, 30)


@fixture(scope="module")
def customer_data():
    return get_customer_data()


@fixture
def ticket_booking_center():
    return TicketBookingCenter(2, 4, 30)


def test_get_customer_data():
    assert isinstance(get_customer_data(), list)


def test_issue_ticket(counter: Counter):
    ticket = counter.issue_ticket(get_customer_data()[0])
    assert isinstance(ticket, Ticket)


def test_orchestrate(ticket_booking_center: TicketBookingCenter, customer_data: list[Customer], mocker: MockFixture):
    ticket_booking_center.counters = [mocker.MagicMock()]
    customer_data = [customer_data[0]]
    customer_data[0].tickets = [Ticket(issue_time=datetime.datetime.now(), issued_at_counter="C1")]
    value = ticket_booking_center.orchestrate(customer_data)
    assert isinstance(value, list)
