import random, time
from datetime import datetime


def generate_log():
    """
    Simulates a log entry. If is_anomaly is True, generates an anomalous log.
    :param is_anomaly:
    :return:
    """

    timestamp = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"), # time
    level = "INFO"
    is_anomaly = False

    latency = random.gauss(100,25)

    if random.random() < 0.1:
        latency = random.gauss(random.choice([300, 400, 500, 600]), 80)
        level = "ERROR"
        is_anomaly = True

        if random.random() < 0.3:
            latency *= random.uniform(1.2, 1.8)

    return {
        "timestamp": timestamp,
        "latency_ms": max(0, latency),
        "level": level,
        "is_anomaly": is_anomaly
    }

if __name__ == "__main__":
    start = time.time()
    while True:
        elapsed = time.time() - start

        anomaly_mode = int(elapsed) % 30 < 5 # every 15 seconds, 5 seconds of anomalies
        log = generate_log(is_anomaly=anomaly_mode)
        print(log)
        time.sleep(0.2)