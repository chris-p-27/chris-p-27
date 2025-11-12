# Runbook — Ubidots (device, dashboard, alerts)

1) Crea cuenta en Ubidots Industrial y copia tu **Token**.
2) Crea **Device** con label `aquarium_iteration_01`.
3) (Opc.) Pre-crea variables (si no, se crean en la primera publicación).
4) Crea **Dashboard**:
   - Gauges/Line charts para `water_temp_c`, `water_ph`.
   - Indicator para `water_level_status` y `ato_status`.
5) Crea **Events**:
   - Umbral pH fuera de [6.2, 8.2] durante 5 min → notificación (email/app).
   - Inactividad: >10 min sin datos → notificación.
6) **Control**: agrega widget para `ato_mode_cmd` (switch/enum) y documenta el **SUB_TOPIC** que usará el dispositivo para cambios por MQTT (según doc vigente de Ubidots).
7) Guarda capturas y/o exportables en `cloud/ubidots/`.
