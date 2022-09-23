import functools
import logging
import threading

import pika

# broker_ip = 'localhost'
from logger_funcs import color_logger

broker_port = 5672

user = '*********'
password = '*********'


# LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
#               '-35s %(lineno) -5d: %(message)s')
# LOGGER = logging.getLogger(__name__)
#
# logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def ack_message(ch, delivery_tag):
    """Note that `ch` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def do_work(conn, ch, delivery_tag, body, do_function, initArgs):
    thread_id = threading.get_ident()
    # LOGGER.info('Thread id: %s Delivery tag: %s Message body: %s', thread_id,
    #             delivery_tag, body)
    # Sleeping to simulate 10 seconds of work
    print(body)
    do_function(body.decode("utf-8"), initArgs)
    cb = functools.partial(ack_message, ch, delivery_tag)
    conn.add_callback_threadsafe(cb)


def on_message(ch, method_frame, _header_frame, body, args):
    (conn, thrds, do_function, initArgs) = args
    delivery_tag = method_frame.delivery_tag

    t = threading.Thread(target=do_work,
                         args=(conn, ch, delivery_tag, body, do_function, initArgs))
    t.start()
    thrds.append(t)
    print('Active number of threads are ', threading.active_count())
    while threading.active_count() > 5:
        ch._connection.sleep(10.0)


def start_consume(ch):
    try:
        ch.start_consuming()
    except pika.exceptions.AMQPHeartbeatTimeout:
        start_consume(ch)
    except KeyboardInterrupt:
        ch.stop_consuming()


def receive(broker_ip, queue_name, do_function, initArgs):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(broker_ip,
                                           broker_port,
                                           '/',
                                           credentials,
                                           heartbeat=60)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=4)

    threads = []
    on_message_callback = functools.partial(on_message, args=(
    connection, threads, do_function, initArgs))

    channel.basic_consume(queue_name,
                          on_message_callback)

    try:
        channel.start_consuming()
    # except pika.exceptions.AMQPHeartbeatTimeout:
    #     channel.stop_consuming()
    #     start_consume(channel)
    except KeyboardInterrupt:
        channel.stop_consuming()

    for thread in threads:
        thread.join()

    connection.close()
