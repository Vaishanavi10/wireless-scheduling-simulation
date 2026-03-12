import random
import matplotlib.pyplot as plt

# basic simulation parameters
SIM_TIME = 2000
NUM_DEVICES = 30
BUFFER_LIMIT = 100


# simple packet structure
class Packet:
    def __init__(self, arrival_time, priority):
        self.arrival_time = arrival_time
        self.priority = priority
        self.service_time = None


# device that generates packets
class Device:
    def __init__(self, device_id, traffic_type):
        self.device_id = device_id
        self.traffic_type = traffic_type

    def generate_packet(self, current_time):

        r = random.random()

        # different traffic rates depending on priority
        if self.traffic_type == "HIGH" and r < 0.4:
            return Packet(current_time, "HIGH")

        if self.traffic_type == "MEDIUM" and r < 0.3:
            return Packet(current_time, "MEDIUM")

        if self.traffic_type == "LOW" and r < 0.2:
            return Packet(current_time, "LOW")

        return None


# create devices with different traffic types
def create_devices():

    devices = []

    for i in range(NUM_DEVICES):

        if i < 10:
            devices.append(Device(i, "HIGH"))

        elif i < 20:
            devices.append(Device(i, "MEDIUM"))

        else:
            devices.append(Device(i, "LOW"))

    return devices


# strict priority scheduler
def simulate_strict_priority():

    devices = create_devices()

    high_queue = []
    med_queue = []
    low_queue = []

    delays = {"HIGH": [], "MEDIUM": [], "LOW": []}
    drops = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for t in range(SIM_TIME):

        # generate packets
        for d in devices:

            pkt = d.generate_packet(t)

            if pkt:

                if pkt.priority == "HIGH":
                    if len(high_queue) < BUFFER_LIMIT:
                        high_queue.append(pkt)
                    else:
                        drops["HIGH"] += 1

                elif pkt.priority == "MEDIUM":
                    if len(med_queue) < BUFFER_LIMIT:
                        med_queue.append(pkt)
                    else:
                        drops["MEDIUM"] += 1

                else:
                    if len(low_queue) < BUFFER_LIMIT:
                        low_queue.append(pkt)
                    else:
                        drops["LOW"] += 1

        # scheduling decision
        if high_queue:
            pkt = high_queue.pop(0)

        elif med_queue:
            pkt = med_queue.pop(0)

        elif low_queue:
            pkt = low_queue.pop(0)

        else:
            continue

        pkt.service_time = t
        delay = pkt.service_time - pkt.arrival_time
        delays[pkt.priority].append(delay)

    return delays, drops


# round robin scheduler
def simulate_round_robin():

    devices = create_devices()

    queues = {"HIGH": [], "MEDIUM": [], "LOW": []}

    delays = {"HIGH": [], "MEDIUM": [], "LOW": []}
    drops = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    order = ["HIGH", "MEDIUM", "LOW"]
    index = 0

    for t in range(SIM_TIME):

        # packet generation
        for d in devices:

            pkt = d.generate_packet(t)

            if pkt:
                if len(queues[pkt.priority]) < BUFFER_LIMIT:
                    queues[pkt.priority].append(pkt)
                else:
                    drops[pkt.priority] += 1

        served = False

        # round robin service
        for _ in range(3):

            pr = order[index]
            index = (index + 1) % 3

            if queues[pr]:

                pkt = queues[pr].pop(0)

                pkt.service_time = t
                delay = pkt.service_time - pkt.arrival_time

                delays[pkt.priority].append(delay)

                served = True
                break

        if not served:
            continue

    return delays, drops


# run simulations
sp_delays, sp_drops = simulate_strict_priority()
rr_delays, rr_drops = simulate_round_robin()


# compute average delay
def avg_delay(delay_dict):

    result = {}

    for k in delay_dict:

        if len(delay_dict[k]) > 0:
            result[k] = sum(delay_dict[k]) / len(delay_dict[k])
        else:
            result[k] = 0

    return result


sp_avg = avg_delay(sp_delays)
rr_avg = avg_delay(rr_delays)


# print results
print("---- Strict Priority ----")
print("Average Delay:", sp_avg)
print("Packet Drops:", sp_drops)

print("\n---- Round Robin ----")
print("Average Delay:", rr_avg)
print("Packet Drops:", rr_drops)


# plot delay comparison
labels = ["HIGH", "MEDIUM", "LOW"]

sp_vals = [sp_avg[x] for x in labels]
rr_vals = [rr_avg[x] for x in labels]

x = range(len(labels))

plt.figure()
plt.bar(x, sp_vals)
plt.xticks(x, labels)
plt.title("Strict Priority Delay")
plt.ylabel("Delay")
plt.show()

plt.figure()
plt.bar(x, rr_vals)
plt.xticks(x, labels)
plt.title("Round Robin Delay")
plt.ylabel("Delay")
plt.show()
