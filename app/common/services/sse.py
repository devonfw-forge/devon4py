import logging
import uuid
from asyncio import Queue, CancelledError
from typing import Dict, Iterable

from sse_starlette.sse import EventSourceResponse

logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Class for asynchronous event publishing and sending using Server Sent Events.
    WARNING: Currently this class is not supported with multiple worker nodes.
    """
    def __init__(self):
        self.subscribers: Dict[uuid.UUID, Queue] = dict()

    def publish(self, data, topic: None | str = None, targets: None | Iterable[uuid.UUID] = None) -> None:
        event = {"data": data}
        if isinstance(topic, str):
            event["event"] = topic
        queues_to_update = self.subscribers.values() if not targets else (self.subscribers[key] for key in targets)
        for event_queue in queues_to_update:
            event_queue.put_nowait(event)

    def subscribe(self) -> (uuid.UUID, EventSourceResponse):
        subscriber_id = self._generate_id()
        logger.debug(f"Adding new subscriber with {subscriber_id=}")
        event_queue = Queue()
        self.subscribers[subscriber_id] = event_queue
        return subscriber_id, EventSourceResponse(self._event_generator(subscriber_id, event_queue))

    def unsubscribe(self, subscriber_id: uuid.UUID):
        self.subscribers.pop(subscriber_id)

    def _generate_id(self) -> uuid.UUID:
        subscriber_id = uuid.uuid4()
        while subscriber_id in self.subscribers:
            subscriber_id = uuid.uuid4()
        return subscriber_id

    async def _event_generator(self, subscriber_id: uuid.UUID, event_queue: Queue):
        while True:
            try:
                yield await event_queue.get()
            except CancelledError:
                logger.debug(f"Unsubscribing {subscriber_id=}")
                self.unsubscribe(subscriber_id)
                return
