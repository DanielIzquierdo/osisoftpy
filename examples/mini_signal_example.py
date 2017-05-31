import random, inspect
from sched import scheduler
from time import time, sleep

####################################################################################################
# Minimal implementation of the signaling library
class Signal(object):
    def __init__(self, name):
        self.name = name
        self.receivers = {}
    # This is all we need for a callback function to be registered for a signal:
    def connect(self, receiver):
        self.receivers.setdefault(id(receiver), receiver)
        return receiver
    # When a person expends effort and call their signal.send(), they really iterate through their
    # receivers (callback functions) and __call__() each one, sending it themselves and ++kwargs
    def send(self, sender, **kwargs):
        if not self.receivers:
            return []
        return [(receiver, receiver(sender, **kwargs)) for k, receiver in self.receivers.items()]

# Makes Signals(name) singletons
class Namespace(dict):
    def signal(self, name):
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, Signal(name))

signal = Namespace().signal

####################################################################################################
## Minimal implementation of a Person class,
class Person(object):
    def __init__(self, name):
        self.name = name
        self._energy = 100
    @property
    def energy(self):
        return self._energy
    def work(self):
        effort = random.randint(-10, 10)
        self._energy += effort
        # People will emit a signal when they expend effort
        if effort != 0:
            # the signal will call the callback functon provided by the receiver on connect()
            signal(self.name).send(self, effort=effort)

####################################################################################################
## Now the script - Let's start with the function we'll call to subscribe to signals and callback

## Subscribing to signals
def monitor_changes_in_effort(people):
    # For each person, we call the signal method. signal() will either return an existing signal for
    # that person, or return a new signal for that person. - hence the singletome comment above.
    signals = [signal(person.name) for person in people]

    # for each signal we just got, let's connect to it and tell it what callback function we want
    # to have executed when the signal is emitted.
    [s.connect(track_work) for s in signals]

# This is our callback function - we send this to the signal as the callback that we want executed.
# this will handle the signal that the person sends - we know fro mthe person class that when a
# person expends effort, then emit a signal, and pass in themselves and amount of effort  expended.
def track_work(sender, effort):
    verb = 'rose' if effort > 0 else 'dropped'
    if sender.energy < 100 and sender not in hardworkers:
        hardworkers.add(sender)
    else:
        hardworkers.discard(sender)

# Creating the people objects from a list of names
people = [Person(name) for name in ['ye', 'bryan', 'andrew']]

## Set we'll add people whose energy levels have changed
hardworkers = set([])

# Observing the people we just created
monitor_changes_in_effort(people)

# Starting a 2 second loop that makes each person work 20 times
start_time = time()
duration = 0.5
interval = duration / 20
while time() < start_time + duration:
    [person.work() for person in people]
    sleep(interval - ((time() - start_time) % interval))

# print the list of people who were found to have worked:
print '\n\nThe following people finished the day with less energy than they started:\n'
for person in hardworkers:
    print person.name
print '\n'

# and that's the gist of things.