#!/usr/bin/env python3
#
# Author: Richard Grünert, 2023
#

from enum import Enum
from collections import deque
import sys
import csv


class Event:
    def __init__(self, start_time, callback):
        self.start_time = start_time
        self.callback = callback


class EventList(deque):
    """
    Verkettete Liste zum Sortieren der Ereignisse
    sortiert nach aufsteigender Zeit (früheste Ereignisse sind "links")
    """
    def __init__(self):
        super().__init__(self)

    def add_event(self, event):
        """
        Fügt der Eventliste ein Event-Objekt an der geeigneten Position hinzu
        """
        if len(self) == 0:
            self.appendleft(event)
            return

        i = 0
        for node in self:
            if event.start_time <= node.start_time:
                self.insert(i, event)
                return
            i += 1

        self.append(event)

    def pop_next_event(self):
        """
        Entfernt das nächste (linke) Ereignis der Liste und gibt es zurück
        """
        return self.popleft()


class Scheduler2Phase:
    """
    Scheduler Klasse ohne bedingte Ereignisse
    """
    def __init__(self, sim_state):
        self.sim_state = sim_state
        self.event_list = EventList()
        self.current_time = 0.0
        self.terminated = False

    def terminate(self):
        """
        Teilt dem Scheduler mit, im nächsten Simulationsschritt zu terminieren
        """
        self.terminated = True

    def schedule(self, event):
        """
        Fügt der Ereignisliste ein Ereignisobjekt hinzu, sofern es nicht
        in der Vergangenheit liegt
        """
        if event.start_time < self.current_time:
            raise ValueError('Cannot schedule an event in the past')

        self.event_list.add_event(event)

    def simulate_step(self):
        """
        Führt einen einzelnen Simulationsschritt aus, bestehend aus
        - Terminierung prüfen
        - nächstes Ereignis holen
        - Simulationszeit erhöhen
        - Eventfunktionen aufrufen

        Gibt "False" zurück, wenn der Schritt zur Terminierung geführt hat
        ansonsten "True"
        """

        if self.terminated:
            return False

        if len(self.event_list) == 0:
            return False

        event = self.event_list.pop_next_event()

        self.current_time = event.start_time

        event.callback(self)

        return True

# =========================================

class TrafficLightStates(Enum):
    """
    Codierung für die Ampelzustände
    """
    RED = 0
    GREEN = 1


class TrafficLightSimulationState:
    """
    Hält alle Zustandsvariablen
    """
    def __init__(self):
        self.traffic_light_state = None


def state_red_function(scheduler):
    """
    Funktion, die mit dem Ereignis "Wechsel zu Rot" ausgeführt wird
    """

    scheduler.sim_state.traffic_light_state = TrafficLightStates.RED

    scheduler.schedule(Event(
        scheduler.current_time + 180.12345,
        state_green_function))


def state_green_function(scheduler):
    """
    Funktion, die mit dem Ereignis "Wechsel zu Grün" ausgeführt wird
    """

    scheduler.sim_state.traffic_light_state = TrafficLightStates.GREEN

    scheduler.schedule(
        Event(scheduler.current_time + 60.56789,
              state_red_function))


def state_terminate_function(scheduler):
    """
    Funktion, die mit dem Terminierungs-Ereignis ausgeführt wird
    """

    scheduler.terminate()

# =========================================

if __name__ == "__main__":

    sim_state = TrafficLightSimulationState()

    my_scheduler = Scheduler2Phase(sim_state)

    my_scheduler.schedule(Event(0.0, state_red_function))
    my_scheduler.schedule(Event(1.8144e6, state_terminate_function))

    # write result to csv
    writer = csv.writer(sys.stdout)

    writer.writerow(["time", "state"])

    while my_scheduler.simulate_step() is not False:

        if not my_scheduler.terminated:
            writer.writerow([
                my_scheduler.current_time,
                my_scheduler.sim_state.traffic_light_state
            ])
