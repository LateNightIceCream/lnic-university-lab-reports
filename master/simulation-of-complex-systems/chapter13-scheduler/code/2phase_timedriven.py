#!/usr/bin/env python3
#
# Author: Richard Grünert, 2023
#

from enum import Enum
from collections import deque
import sys
import csv


class Event:
    def __init__(self, start_time, execute_fcn):
        self.start_time = start_time
        self.execute = execute_fcn


class EventList(deque):
    def __init__(self):
        super().__init__(self)

    def add_event(self, event):
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
        return self.popleft()


class SchedulerTimeDriven:
    def __init__(self, sim_state, time_step):
        self.sim_state = sim_state
        self.time_step = time_step
        self.event_list = EventList()
        self.current_time = 0.0
        self.terminated = False

    def terminate(self):
        self.terminated = True

    def schedule(self, event):
        if event.start_time < self.current_time:
            raise ValueError('Cannot schedule an event in the past')

        self.event_list.add_event(event)

    def simulate_step(self):

        if self.terminated:
            return False

        if len(self.event_list) == 0:
            return False

        while self.event_list[0].start_time < self.current_time:
            event = self.event_list.pop_next_event()
            event.execute(self)

        self.current_time += time_step

        return True

# ===============================

class TrafficLightStates(Enum):
    RED = 0
    GREEN = 1


class TrafficLightSimulationState:
    def __init__(self, initial):
        self.traffic_light_state = initial


def state_red_function(scheduler):

    scheduler.sim_state.traffic_light_state = TrafficLightStates.RED

    scheduler.schedule(Event(
        scheduler.current_time + 180.12345,
        state_green_function))


def state_green_function(scheduler):

    scheduler.sim_state.traffic_light_state = TrafficLightStates.GREEN

    scheduler.schedule(
        Event(scheduler.current_time + 60.56789,
              state_red_function))


def state_terminate_function(scheduler):

    print("terminated")

    scheduler.terminate()

# ===============================

if __name__ == "__main__":

    sim_state = TrafficLightSimulationState(TrafficLightStates.RED)

    time_step = 1.0

    my_scheduler = SchedulerTimeDriven(sim_state, time_step)

    my_scheduler.schedule(Event(0, state_red_function))
    my_scheduler.schedule(Event(600.0, state_terminate_function))

    # write result to csv
    writer = csv.writer(sys.stdout)

    writer.writerow(["time", "state"])

    while my_scheduler.simulate_step() is not False:

        if not my_scheduler.terminated:
            writer.writerow([
                my_scheduler.current_time,
                my_scheduler.sim_state.traffic_light_state
            ])
