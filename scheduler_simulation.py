import random
import matplotlib.pyplot as plt

# simple packet class
class Packet:
    def __init__(self, arrival_time, priority):
        self.arrival_time = arrival_time
        self.priority = priority


# generate traffic packets
def generate_packets(num_packets):
    packets = []
    for i in range(num_packets):
        arrival = random.randint(0, 50)

        # randomly assign priority
        priority = random.choice(["HIGH", "MEDIUM", "LOW"])

        packets.append(Packet(arrival, priority))

    return packets


# strict priority scheduler
def strict_priority_scheduler(packets):

    high = [p for p in packets if p.priority == "HIGH"]
    medium = [p for p in packets if p.priority == "MEDIUM"]
    low = [p for p in packets if p.priority == "LOW"]

    queue = high + medium + low

    current_time = 0
    delays = []

    for packet in queue:
        start_time = max(current_time, packet.arrival_time)
        delay = start_time - packet.arrival_time
        delays.append(delay)
        current_time = start_time + 1

    return delays


# round robin scheduler
def round_robin_scheduler(packets):

    high = [p for p in packets if p.priority == "HIGH"]
    medium = [p for p in packets if p.priority == "MEDIUM"]
    low = [p for p in packets if p.priority == "LOW"]

    queues = [high, medium, low]

    current_time = 0
    delays = []

    while any(queues):

        for q in queues:
            if q:
                packet = q.pop(0)
                start_time = max(current_time, packet.arrival_time)
                delay = start_time - packet.arrival_time
                delays.append(delay)
                current_time = start_time + 1

    return delays


# main simulation
packets = generate_packets(100)

sp_delays = strict_priority_scheduler(packets.copy())
rr_delays = round_robin_scheduler(packets.copy())

print("Average delay (Strict Priority):", sum(sp_delays) / len(sp_delays))
print("Average delay (Round Robin):", sum(rr_delays) / len(rr_delays))


# visualize results
labels = ["Strict Priority", "Round Robin"]
values = [sum(sp_delays)/len(sp_delays), sum(rr_delays)/len(rr_delays)]

plt.bar(labels, values)
plt.ylabel("Average Packet Delay")
plt.title("Scheduler Delay Comparison")
plt.show()
