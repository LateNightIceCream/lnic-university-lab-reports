#!/usr/bin/env python3
#
# Author: Richard Grünert, 2023
#

from enum import Enum
from collections import deque
import random
import sys
import csv


class Event:
    """
    Ein Event hält Referenzen auf eine auszuführende Funktion sowie
    optional auf eine Bedingungsfunktion.
    """
    def __init__(self, execute_fcn, condition_fcn = None):
        self.execute = execute_fcn
        self.condition_fcn = condition_fcn


class EventNotice:
    """
    Ein EventNotice stellt einen Eintrag in der EventList dar.
    Es hält das Event und die Zeit, zu der es ausgeführt werden
    soll.
    """
    def __init__(self, event, start_time):
        self.event = event
        self.start_time = start_time


class EventList(deque):
    """
    Die EventList hält EventNotice-Objekte.
    Sie ist sortiert nach der Eintrittszeit des Events.
    Das zeitlich näheste Event ist "links" / vorne
    in der Liste.
    """
    def __init__(self):
        super().__init__(self)

    def add_event_notice(self, notice):

        if len(self) == 0:
            self.appendleft(notice)
            return

        i = 0
        for node in self:
            if notice.start_time <= node.start_time:
                self.insert(i, notice)
                return
            i += 1

        self.append(notice)

    def pop_next_notice(self):
        return self.popleft()


class Scheduler3Phase:
    """
    Notices werden nur gescheduled, wenn ihre Bedinung
    zum schedule-Zeitupunkt erfüllt ist
    """
    def __init__(self, sim_state):
        self.sim_state = sim_state
        self.event_list = EventList()
        self.current_time = 0.0
        self.terminated = False

    def terminate(self):
        self.terminated = True

    def schedule(self, start_time, event):
        if start_time < self.current_time:
            raise ValueError('Cannot schedule an event in the past')

        if event.condition_fcn is not None\
           and event.condition_fcn(self.sim_state) is False:
            return

        self.event_list.add_event_notice(EventNotice(event, start_time))

    def simulate_step(self):

        if self.terminated:
            return False

        if len(self.event_list) == 0:
            return False

        notice = self.event_list.pop_next_notice()

        self.current_time = notice.start_time
        notice.event.execute(self)

        return True

# ============================

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
        self.previous_traffic_light_state = None
        self.waiting = None
        self.red_red_transitions = 0
        self.red_green_transitions = 0


def state_red_conditional_function(scheduler):
    if scheduler.sim_state.waiting < 0.5:
        state_red_function(scheduler)
        scheduler.sim_state.red_red_transitions += 1
    else:
        state_green_function(scheduler)
        scheduler.sim_state.red_green_transitions += 1


def are_enough_people_waiting(sim_state):
    return sim_state.waiting > 0.5


def state_red_function(scheduler):
    """
    Funktion, die mit dem Ereignis "Wechsel zu Rot" ausgeführt wird
    """
    scheduler.sim_state.traffic_light_state = TrafficLightStates.RED

    prev_state = scheduler.sim_state.previous_traffic_light_state

    # Übergänge zählen für Auswertung
    if prev_state is not None:
        if prev_state is TrafficLightStates.RED:
            scheduler.sim_state.red_red_transitions += 1
        else:
            scheduler.sim_state.red_green_transitions += 1

    scheduler.sim_state.waiting = random.uniform(0.0, 1.0)

    scheduler.schedule(
        scheduler.current_time + 180.12345,
        Event(state_green_function, are_enough_people_waiting))

    scheduler.schedule(
        scheduler.current_time + 180.12345,
        Event(state_red_function,
              lambda sim_state: not are_enough_people_waiting(sim_state)))

    scheduler.sim_state.previous_traffic_light_state = TrafficLightStates.RED

    ## Alternativ: mit Hilfsereignis
    # scheduler.schedule(
    #     scheduler.current_time + 180.12345,
    #     Event(state_red_conditional_function))


def state_green_function(scheduler):
    """
    Funktion, die mit dem Ereignis "Wechsel zu Grün" ausgeführt wird
    """
    scheduler.sim_state.traffic_light_state = TrafficLightStates.GREEN

    scheduler.schedule(
        scheduler.current_time + 60.56789,
        Event(state_red_function))

    scheduler.sim_state.previous_traffic_light_state = TrafficLightStates.GREEN


def state_terminate_function(scheduler):
    """
    Funktion, die mit dem Terminierungs-Ereignis ausgeführt wird
    """
    scheduler.terminate()

# ============================

if __name__ == "__main__":

    #random.seed(123)

    sim_state = TrafficLightSimulationState()

    my_scheduler = Scheduler3Phase(sim_state)

    my_scheduler.schedule(0.0, Event(state_red_function))
    my_scheduler.schedule(600.0, Event(state_terminate_function))

    # write result to csv
    writer = csv.writer(sys.stdout)

    writer.writerow(["time", "state"])

    while my_scheduler.simulate_step() is not False:

        if not my_scheduler.terminated:
            writer.writerow([
                my_scheduler.current_time,
                my_scheduler.sim_state.traffic_light_state
            ])

    print(my_scheduler.sim_state.red_red_transitions)
    print(my_scheduler.sim_state.red_green_transitions)
    print(my_scheduler.sim_state.red_green_transitions
          / my_scheduler.sim_state.red_red_transitions)
