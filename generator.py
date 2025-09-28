import random, time

SERVICES = ["auth", "payments", "db"]

def generate_log(is_anomaly=False):
    """
    Simulates a log entry. If is_anomaly is True, generates an anomalous log.
    :param is_anomaly:
    :return:
    """

    log = {
        "timestamp": time.time(), # time
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