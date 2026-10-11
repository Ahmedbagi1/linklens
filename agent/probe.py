import subprocess


def get_default_gateway():
    result = subprocess.run(
        ["route", "-n", "get", "default"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        if line.strip().startswith("gateway:"):
            return line.split(":", 1)[1].strip()

    return None


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


def display_results(target, packet_loss, average_latency):
    print(f"Target: {target}")
    print(f"Packet loss: {packet_loss}%")
    print(f"Average latency: {average_latency} ms")
    print()


print("LinkLens Network Probe")
print("----------------------")

gateway = get_default_gateway()

if gateway:
    print("Local Network")
    display_results(gateway, *measure_ping(gateway))
else:
    print("Could not detect default gateway.\n")

print("Internet Connection")
display_results("1.1.1.1", *measure_ping("1.1.1.1"))
display_results("8.8.8.8", *measure_ping("8.8.8.8"))