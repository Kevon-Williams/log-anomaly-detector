import random, time
from datetime import datetime

SERVICES = ["auth", "payments", "db"]

def generate_log(is_anomaly=False):
    """
    Simulates a log entry. If is_anomaly is True, generates an anomalous log.
    :param is_anomaly:
    :return:
    """

    log = {
        "timestamp": datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"), # time
        "service": random.choice(SERVICES),
        "latency_milisecs": random.gauss(100, 15), #normal latency is 100ms +- 15ms
        "level": "INFO",  # default log level

    }

    if is_anomaly:
        log["latency_milisecs"] = random.gauss(600, 30),
        log["level"] = "ERROR"
        log["msg"] = random.choice([500, 502, 503, 504])
    else:
        log["msg"] = "Service running normally"

    return log

if __name__ == "__main__":
    start = time.time()
    while True:
        elapsed = time.time() - start

        anomaly_mode = int(elapsed) % 15 < 5 # every 15 seconds, 5 seconds of anomalies
        log = generate_log(is_anomaly=anomaly_mode)
        print(log)
        time.sleep(0.2)