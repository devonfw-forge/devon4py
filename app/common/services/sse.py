import logging
import uuid
from asyncio import Queue, CancelledError
from typing import Dict

from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request

logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self):
        self.subscribers: Dict[uuid.UUID, Queue] = dict()

    async def publish(self, data, topic: None | str = None):
        event = {"data": data}
        if isinstance(topic, str):
            event["event"] = topic
        for event_queue in self.subscribers.values():
            await event_queue.put(event)

    def subscribe(self, request: Request, subscriber_id=None) -> EventSourceResponse:
        if not subscriber_id:
            subscriber_id = uuid.uuid4()
        logger.debug(f"Adding new subscriber with {subscriber_id=}")
        event_queue = Queue()
        self.subscribers[subscriber_id] = event_queue
        return EventSourceResponse(self._event_generator(subscriber_id, event_queue, request))

    def unsubscribe(self, subscriber_id):
        self.subscribers.pop(subscriber_id)

    async def _event_generator(self, subscriber_id, event_queue: Queue, request: Request):
        while True:
            try:
                yield await event_queue.get()
            except CancelledError:
                logger.debug(f"Unsubscribing {subscriber_id=}")
                self.unsubscribe(subscriber_id)
                return
