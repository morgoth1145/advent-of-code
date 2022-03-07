import collections
import threading

class ChannelClosed(Exception):
    pass

class BufferedChannel:
    '''Buffered pipe to connect concurrent processing in separate threads.
    Supports sending and receiving arbitrary messages. When given a maximum size,
    send calls will block when the pending messages buffer is full. Similarly,
    recv calls will block if the pending messages buffer is empty.

    When closed any waiting send/recv calls will raise a ChannelClosed exception.
    Future send calls will also raise a ChannelClosed exception.
    If the pending messages buffer is not empty, future recv calls will pull
    from the buffer and return the pending message. Once the buffer is empty,
    recv calls will also raise a ChannelClosed exception.

    Also supports iteration. Such usage will wait for (and return) sent messages
    until the channel is closed.
    '''
    def __init__(self, max_size=0):
        self.__mutex = threading.RLock()
        self.__send_cv = threading.Condition(self.__mutex)
        self.__recv_cv = threading.Condition(self.__mutex)
        self.__closed = False
        self.__queue = collections.deque()
        self.__max_size = max_size

        self.__on_send = []
        self.__on_recv = []

    def _add_send_event_listener(self, fn):
        self.__on_send.append(fn)

    def _add_recv_event_listener(self, fn):
        self.__on_recv.append(fn)

    def send(self, val):
        with self.__mutex:
            for fn in self.__on_send:
                fn()
            if self.__max_size:
                self.__send_cv.wait_for(lambda: self.__closed or
                                        len(self.__queue) < self.__max_size)
            if self.__closed:
                raise ChannelClosed()
            self.__queue.append(val)
            self.__recv_cv.notify()

    def recv(self):
        with self.__mutex:
            for fn in self.__on_recv:
                fn()
            self.__recv_cv.wait_for(lambda: self.__closed or
                                    len(self.__queue) > 0)
            if self.__closed and len(self.__queue) == 0:
                raise ChannelClosed()
            val = self.__queue.popleft()
            self.__send_cv.notify()
            return val

    def close(self):
        with self.__mutex:
            self.__closed = True
            self.__send_cv.notify_all()
            self.__recv_cv.notify_all()

    def __iter__(self):
        try:
            while True:
                yield self.recv()
        except ChannelClosed:
            pass # And we're done!

class SyncChannel:
    '''Synchronous pipe to connect concurrent processing in separate threads.
    Supports sending and receiving arbitrary messages. Both send and recv calls
    will block until they are paired together.

    When closed any waiting send/recv calls will raise a ChannelClosed exception,
    as well as any future send/recv calls.

    Also supports iteration. Such usage will wait for (and return) sent messages
    until the channel is closed.
    '''
    def __init__(self):
        self.__mutex = threading.RLock()
        self.__send_cv = threading.Condition(self.__mutex)
        self.__recv_cv = threading.Condition(self.__mutex)
        self.__handoff_cv = threading.Condition(self.__mutex)
        self.__closed = False
        self.__send_state = 0
        self.__recv_state = 0
        self.__val = None

        self.__on_send = []
        self.__on_recv = []

    def _add_send_event_listener(self, fn):
        self.__on_send.append(fn)

    def _add_recv_event_listener(self, fn):
        self.__on_recv.append(fn)

    def send(self, val):
        with self.__mutex:
            for fn in self.__on_send:
                fn()
            self.__send_cv.wait_for(lambda: self.__closed or
                                    self.__send_state == 0)
            if self.__closed:
                raise ChannelClosed()
            self.__send_state = 1
            self.__handoff_cv.wait_for(lambda: self.__closed or
                                       self.__recv_state != 0)
            if self.__closed:
                raise ChannelClosed()
            self.__val = val
            self.__send_state = 2
            self.__handoff_cv.notify()

    def recv(self):
        with self.__mutex:
            for fn in self.__on_recv:
                fn()
            self.__recv_cv.wait_for(lambda: self.__closed or
                                    self.__recv_state == 0)
            if self.__closed:
                raise ChannelClosed()
            self.__recv_state = 1
            if self.__send_state == 1:
                self.__handoff_cv.notify()
            self.__handoff_cv.wait_for(lambda: self.__closed or
                                       self.__send_state == 2)
            if self.__closed and self.__send_state != 2:
                raise ChannelClosed()
            val = self.__val
            self.__send_state = 0
            self.__recv_state = 0
            self.__send_cv.notify()
            self.__recv_cv.notify()
            return val

    def close(self):
        with self.__mutex:
            self.__closed = True
            self.__send_cv.notify_all()
            self.__recv_cv.notify_all()
            self.__handoff_cv.notify_all()

    def __iter__(self):
        try:
            while True:
                yield self.recv()
        except ChannelClosed:
            pass # And we're done!

class _ChannelMessageStats:
    def __init__(self):
        self.sends = 0
        self.receives = 0

    def _on_send(self):
        self.sends += 1

    def _on_recv(self):
        self.receives += 1

def record_message_stats(channel):
    '''Sets up an object to record send and recv counts on a channel.
    Current counts can be retrieved via the "sends" and "receives" members
    on the returned stats object.
    '''
    stats = _ChannelMessageStats()
    channel._add_send_event_listener(stats._on_send)
    channel._add_recv_event_listener(stats._on_recv)
    return stats

def detect_deadlock_events(thread_count, *channels):
    '''Sets up deadlock detection for a set of channels. As this internally
    tracks send and recv events this must be called prior to any messages being
    sent on the channels in question.

    Returns a SyncChannel which will be sent 'deadlock' any time the channels
    reach deadlock. This may occur multiple times if the deadlock is resolved.

    Arguments:
    thread_count -- The number of threads in play which must be waiting for
    deadlock to occur
    channels -- All the channels in play in the system which may deadlock
    '''
    deadlock_events = SyncChannel()

    mutex = threading.RLock()

    waiting_receives = 0
    def on_send():
        nonlocal waiting_receives
        with mutex:
            waiting_receives -= 1
    def on_recv():
        nonlocal waiting_receives
        with mutex:
            waiting_receives += 1
            if waiting_receives == thread_count:
                deadlock_events.send('deadlock')

    for chan in channels:
        chan._add_send_event_listener(on_send)
        chan._add_recv_event_listener(on_recv)

    return deadlock_events
