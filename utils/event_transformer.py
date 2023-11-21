import pygame

from pygame.event import Event


def convert(events: list[Event]) -> dict[int, list[Event]]:
    """Converts the given events into a dictionary.

        Its keys are the event types and its values are the events of that type.
        It allows to avoid iterating over the events list multiple times.

        :param events: The events to convert.
        :type events: list[Event].

        :return: The converted events.
        :rtype: dict[int, list[Event]].

    """
    converted_events: dict[int, list[Event]] = {pygame.KEYDOWN: [], pygame.QUIT: [], pygame.TEXTINPUT: []}
    for event in events:
        if event.type == pygame.KEYDOWN:
            converted_events.get(pygame.KEYDOWN).append(event.key)
        elif event.type == pygame.QUIT:
            converted_events.get(pygame.QUIT).append(event)
        elif event.type == pygame.TEXTINPUT:
            converted_events.get(pygame.TEXTINPUT).append(event)
    return converted_events
