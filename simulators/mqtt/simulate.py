import os, ssl, json, time, random, threading
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv()

HOST = os.getenv("UBIDOTS_HOST", "industrial.api.ubidots.com")
PORT = int(os.getenv("UBIDOTS_PORT", "8883"))
TOKEN = os.getenv("UBIDOTS_TOKEN")  # MQTT username in Ubidots
DEVICE = os.getenv("UBIDOTS_DEVICE", "aquarium_iteration_01")
PERIOD = int(os.getenv("PUB_PERIOD_SEC", "45"))
TLS_CA = os.getenv("UBIDOTS_TLS_CA")  # optional

UP_TOPIC = f"/v2.0/devices/{DEVICE}"
# TODO: Confirma el tópico de downlink de control según la doc vigente de Ubidots.
# Ajusta esta constante cuando definas el flujo de control:
SUB_TOPIC = f"/v2.0/devices/{DEVICE}/ato_mode_cmd"

client = mqtt.Client(client_id=f"sim-{DEVICE}-{int(time.time())}", clean_session=True, protocol=mqtt.MQTTv311)
client.username_pw_set(TOKEN, password="")  # Ubidots: username=token, password blank

# TLS
ctx = ssl.create_default_context()
if TLS_CA and os.path.exists(TLS_CA):
    ctx.load_verify_locations(TLS_CA)
client.tls_set_context(ctx)
client.tls_insecure_set(False)

def on_connect(cli, userdata, flags, rc):
    print(f"[MQTT] Connected: rc={rc}")
    # Suscripción de control (downlink) — ajusta SUB_TOPIC cuando definas el flujo
    try:
        cli.subscribe(SUB_TOPIC, qos=1)
        print(f"[MQTT] Subscribed to: {SUB_TOPIC}")
    except Exception as e:
        print(f"[MQTT] Subscribe error: {e}")

def on_message(cli, userdata, msg):
    print(f"[MQTT] Downlink topic={msg.topic} payload={msg.payload.decode('utf-8','ignore')}")

def telemetry():
    uptime = 0
    while True:
        uptime += PERIOD
        payload = {
            "water_temp_c": round(24.8 + random.uniform(-0.4, 0.6), 2),
            "water_ph": round(7.20 + random.uniform(-0.05, 0.05), 2),
            "water_level_low_sw": 0,
            "water_level_high_sw": 1,
            "water_level_status": "ok",
            "ato_status": "idle",
            "wifi_rssi_dbm": -60 + random.randint(-5, 5),
            "fw_version": "esp32-fishmod-0.1.0",
            "device_uptime_s": uptime,
            "timestamp": int(time.time() * 1000)
        }
        j = json.dumps(payload, separators=(",", ":"))
        try:
            info = client.publish(UP_TOPIC, payload=j, qos=1, retain=False)
            info.wait_for_publish(timeout=5)
            print(f"[MQTT] Uplink -> {UP_TOPIC} {j}")
        except Exception as e:
            print(f"[MQTT] Publish error: {e}")
        time.sleep(PERIOD)

client.on_connect = on_connect
client.on_message = on_message

print(f"[MQTT] Connecting to {HOST}:{PORT} using TLS 8883 as {TOKEN[:6]}***")
client.connect(HOST, PORT, keepalive=60)

threading.Thread(target=telemetry, daemon=True).start()
client.loop_forever()
