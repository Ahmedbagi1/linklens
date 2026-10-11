import subprocess


def measure_ping(target):
    result = subprocess.run(
        ["ping", "-c", "4", target],
        capture_output=True,
        text=True
    )

    output = result.stdout

    packet_loss = None
    average_latency = None

    for line in output.splitlines():

        if "packet loss" in line:
            packet_loss = float(
                line.split(",")[2]
                .strip()
                .split("%")[0]
            )

        if "round-trip" in line:
            latency_values = line.split("=")[1].strip().split()[0]
            average_latency = float(latency_values.split("/")[1])

    return packet_loss, average_latency


target = "1.1.1.1"

packet_loss, average_latency = measure_ping(target)

print("LinkLens Network Probe")
print("----------------------")
print(f"Target: {target}")
print(f"Packet loss: {packet_loss}%")
print(f"Average latency: {average_latency} ms")