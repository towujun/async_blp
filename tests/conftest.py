"""
All fixtures are samples of blpapi events

For testing purposes, please use `Session.send_event` method that emulates
blpapi and opens another thread. You can also call the needed handler method
directly.
"""
import logging

import pytest

from async_blp.requests import ReferenceDataRequest
from async_blp.utils import log
from async_blp.utils.env_test import CorrelationId
from async_blp.utils.env_test import Element
from async_blp.utils.env_test import Event
from async_blp.utils.env_test import Message
from async_blp.utils.env_test import SessionOptions


# pylint does not like pytest.fixture but we do
# pylint: disable=redefined-outer-name


@pytest.fixture(autouse=True, scope='session')
def debug_logs():
    """
    Show all logs for tests
    """
    log.set_logger(logging.DEBUG)


@pytest.fixture()
def session_options() -> SessionOptions():
    """
    For tests it's not important
    """
    session_options_ = SessionOptions()
    session_options_.setServerHost("localhost")
    session_options_.setServerPort(8194)
    return session_options_


@pytest.fixture()
def data_request():
    """
    Simple request
    """
    field_name = 'PX_LAST'
    security_id = 'F Equity'
    return ReferenceDataRequest([security_id], [field_name])


@pytest.fixture()
def open_session_event():
    """
    SessionStarted event that is the first event that Bloomberg sends,
    indicates that session was successfully opened
    """
    event_ = Event(type_=Event.SESSION_STATUS,
                   msgs=[Message(value=0, name='SessionStarted'), ]
                   )
    return event_


@pytest.fixture()
def stop_session_event():
    """
    SessionStopped event that is the very last event that Bloomberg sends,
    after user calls `session.stopAsync`
    """
    event_ = Event(type_=Event.SESSION_STATUS,
                   msgs=[Message(value=0, name='SessionTerminated',
                                 ),
                         ]
                   )
    return event_


@pytest.fixture()
def open_service_event():
    """
    ServiceOpened event, indicates that service was successfully opened
    """
    event_ = Event(type_=Event.SERVICE_STATUS,
                   msgs=[Message(value=0, name='ServiceOpened',
                                 children={
                                     'serviceName':
                                         Element(
                                             value="//blp/refdata")
                                     }
                                 ), ]
                   )
    return event_


@pytest.fixture()
def element_daily_reached():
    """
    Error indicating that too many requests were made
    """
    return Element(name='subcategory', value='DAILY_LIMIT_REACHED')


@pytest.fixture()
def msg_daily_reached(element_daily_reached):
    """
    Error indicating that too many requests were made
    """
    return Message(name="responseError",
                   value='',
                   children={
                       "responseError": element_daily_reached
                       }
                   )


@pytest.fixture()
def element_monthly_reached():
    """
    Error indicating that too many requests were made
    """
    return Element(name='subcategory', value='MONTHLY_LIMIT_REACHED')


@pytest.fixture()
def error_event(msg_daily_reached):
    """
    Error indicating that too many requests were made
    """
    return Event(type_=Event.RESPONSE,
                 msgs=[
                     msg_daily_reached,
                     ],
                 )


@pytest.fixture()
def non_error_message():
    """
    ???
    """
    return Message(name="validMessage",
                   value='',
                   children={
                       "validMessage": element_daily_reached
                       }
                   )


@pytest.fixture()
def market_data():
    """
    just random data in subscriber
    """
    mk_data = 'INITPAINT'
    bid = 133.75
    ask_size = 1
    ind_bid_flag = False
    return mk_data, bid, ask_size, ind_bid_flag


@pytest.fixture()
def start_subscribe_event():
    """
    SubscriptionStarted = {
        exceptions[] = {
        }
        streamIds[] = {
            "1"
        }
        receivedFrom = {
            address = "localhost:8194"
        }
        reason = "Subscriber made a subscription"
    }
    """
    event_ = Event(type_=Event.SUBSCRIPTION_STATUS,
                   msgs=[Message(value=0, name='SubscriptionStarted'), ]
                   )
    return event_


@pytest.fixture()
def market_data_event(market_data):
    """
    simple example date from subscriber
    """
    mk_data, bid, ask_size, ind_bid_flag = market_data
    msgs = [Message(name="MarketDataEvents",
                    value=[],
                    children={
                        'MarketDataEvents':
                            Element(
                                'MarketDataEvents',
                                value=[],
                                children={
                                    'MKTDATA':      Element('MKTDATA', mk_data),
                                    'BID':          Element("BID", bid),
                                    'ASK_SIZE':     Element('ASK_SIZE',
                                                            ask_size),
                                    'IND_BID_FLAG': Element('IND_BID_FLAG',
                                                            ind_bid_flag)
                                    },
                                )
                        },
                    correlationId=CorrelationId("test"),
                    )]

    return Event(Event.SUBSCRIPTION_DATA, msgs)
