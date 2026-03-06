#!/usr/bin/env python3
import argparse
import json
import ssl
import sys
import time

try:
    import paho.mqtt.client as mqtt
except Exception:
    print("ERROR: missing dependency paho-mqtt.\nInstall with: ./.venv-mqtt/bin/pip install paho-mqtt")
    sys.exit(2)


def safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default


def main():
    p = argparse.ArgumentParser(description="Read Bambu printer status via LAN MQTT")
    p.add_argument("--ip", required=True, help="Printer IP")
    p.add_argument("--code", required=True, help="LAN access code")
    p.add_argument("--sn", required=True, help="Printer serial number")
    p.add_argument("--wait", type=int, default=12, help="Wait seconds for first report")
    args = p.parse_args()

    state = {"connected": False, "rc": None, "payload": None, "topic": None}

    def on_connect(client, userdata, flags, reason_code, properties=None):
        rc = getattr(reason_code, "value", reason_code)
        state["rc"] = rc
        state["connected"] = (rc == 0)
        client.subscribe(f"device/{args.sn}/report", qos=0)

    def on_message(client, userdata, msg):
        state["topic"] = msg.topic
        try:
            state["payload"] = json.loads(msg.payload.decode("utf-8", "ignore"))
        except Exception:
            state["payload"] = {"raw": msg.payload.decode("utf-8", "ignore")}
        client.disconnect()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="openclaw-status")
    client.username_pw_set("bblp", args.code)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    try:
        client.connect(args.ip, 8883, keepalive=20)
    except Exception as e:
        print(f"CONNECT_ERROR: {e!r}")
        sys.exit(1)

    client.loop_start()
    for _ in range(args.wait):
        if state["payload"] is not None:
            break
        time.sleep(1)
    client.loop_stop()

    if not state["connected"]:
        print(f"CONNECT_FAILED rc={state['rc']}")
        sys.exit(1)

    if state["payload"] is None:
        print("CONNECTED_OK_NO_MESSAGE")
        sys.exit(0)

    pld = state["payload"]
    # Bambu report commonly wrapped under print
    info = pld.get("print", pld)

    gcode_state = info.get("gcode_state")
    stage = info.get("mc_percent")
    remain_min = info.get("mc_remaining_time")
    nozzle = info.get("nozzle_temper")
    bed = info.get("bed_temper")

    print("CONNECTED_OK_WITH_MESSAGE")
    print(f"topic: {state['topic']}")
    if gcode_state is not None:
        print(f"state: {gcode_state}")
    if stage is not None:
        print(f"progress: {stage}%")
    if remain_min is not None:
        print(f"remaining: {remain_min} min")
    if nozzle is not None:
        print(f"nozzle: {nozzle}°C")
    if bed is not None:
        print(f"bed: {bed}°C")

    # AMS quick summary (best effort)
    ams = info.get("ams") or {}
    ams_list = ams.get("ams") if isinstance(ams, dict) else None
    if isinstance(ams_list, list) and ams_list:
        a0 = ams_list[0]
        hum = a0.get("humidity")
        temp = a0.get("temp")
        if hum is not None or temp is not None:
            print(f"ams[0]: humidity={hum}, temp={temp}°C")


if __name__ == "__main__":
    main()
