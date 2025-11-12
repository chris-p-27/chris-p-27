# Módulo PECES — Iteración 1 (cloud-first, sin PC 24/7)

**Objetivo:** telemetría y control básico de un acuario piloto (120 L) usando:
- Nodo futuro: **ESP32 + ESPHome** con automatizaciones locales (ATO, umbrales).
- **MQTT** cifrado (**TLS 8883**) contra **Ubidots** (broker + dashboards + alerts).
- **Tailscale** sólo para mantenimiento (VPN segura), no requerido para operar.
- **Device label:** `aquarium_iteration_01`.

Este repo incluye:
- **Contratos de datos** (variables, topics, payloads).
- **Simulador MQTT** (sin hardware): publica telemetría a Ubidots y escucha un tópico de control.
- **Plantilla ESPHome** (YAML) para cuando llegue el ESP32 (sin pines, con comentarios).
- **Runbooks** para Ubidots y Tailscale.

## Cómo probar HOY (sin hardware)
1. Crea un **device** en Ubidots con label `aquarium_iteration_01` (ver `docs/runbooks/ubidots-setup.md`).
2. Duplica `.env.example` a `.env` y completa `UBIDOTS_TOKEN` (no lo subas a Git).
3. Instala dependencias del simulador:
   ```bash
   cd simulators/mqtt
   python -m venv .venv && source .venv/bin/activate  # en Windows: .venv\Scripts\activate
   pip install -r <(python - <<'PY'
print('paho-mqtt\npython-dotenv\n')
PY)
   ```
4. Ejecuta el simulador:
   ```bash
   python simulate.py
```

5. Abre el **dashboard** en Ubidots y verifica `water_temp_c`, `water_ph`, `water_level_status`, `ato_status`.
   Opcional: configura un control para `ato_mode_cmd` y ajusta el **SUB_TOPIC** según docs de Ubidots.

> **Secretos:** usa `.env` local y/o **GitHub Secrets** (si ejecutas el workflow `simulator.yml`). Nunca subas tokens.

## Estructura

* `docs/`: arquitectura, contratos, decisiones y runbooks.
* `simulators/mqtt/`: publicador de ejemplo (uplink) + suscripción de control (downlink).
* `firmware/esp32-fishmod/`: plantilla ESPHome lista para completar pines y calibraciones.

Licencia: ver `LICENSE`.

