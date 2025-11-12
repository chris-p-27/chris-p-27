# Contratos de datos — `aquarium_iteration_01`

## Identidad
- `device_label`: `aquarium_iteration_01`

## Variables (labels y semántica)

### A) Telemetría
| Variable               | Tipo  | Unidad/Valores           | Significado                        |
|---|---|---|---|
| `water_temp_c`         | float | °C                        | Temperatura del agua               |
| `water_ph`             | float | pH                        | pH del agua (calibrado)            |
| `water_level_status`   | str   | `low` \| `ok` \| `high`   | Estado derivado del nivel          |
| `water_level_low_sw`   | int   | `0/1`                     | Sensor crudo de **nivel bajo**     |
| `water_level_high_sw`  | int   | `0/1`                     | Sensor crudo de **nivel alto**     |

### B) Estado de nodo / ATO
| Variable          | Tipo  | Valores                          | Significado                         |
|---|---|---|---|
| `ato_status`      | str   | `idle` \| `filling` \| `lockout` | Estado del ATO                      |
| `wifi_rssi_dbm`   | int   | dBm                               | Señal Wi-Fi                         |
| `fw_version`      | str   | —                                 | Versión de firmware/config          |
| `device_uptime_s` | int   | segundos                          | Tiempo encendido                    |
| `availability`*   | str   | `online` \| `offline`             | Estado (LWT). *opcional*            |

### C) Control (downlink)
| Variable        | Tipo | Valores                | Significado               |
|---|---|---|---|
| `ato_mode_cmd`  | str  | `auto` \| `on` \| `off`| Modo de operación del ATO |

### D) Contexto por tanque (metadatos adjuntos)
- `tank_volume_l` (int), `tank_name` (str), `species_list` (str), `location_label` (str)  
- `ph_target_min`/`ph_target_max` (float), `temp_target_min_c`/`temp_target_max_c` (float)

## MQTT — Uplink (dispositivo → nube)
- **Broker**: `industrial.api.ubidots.com` (TLS **8883**, usuario = **token**)
- **Topic**: `/v2.0/devices/aquarium_iteration_01`
- **Payload (JSON)**:
```json
{
  "water_temp_c": 25.1,
  "water_ph": 7.22,
  "water_level_status": "ok",
  "water_level_low_sw": 0,
  "water_level_high_sw": 1,
  "ato_status": "idle",
  "wifi_rssi_dbm": -60,
  "fw_version": "esp32-fishmod-0.1.0",
  "device_uptime_s": 12345,
  "timestamp": 1731379200000
}
```

## MQTT — Downlink (nube → dispositivo)

* **Variable de control**: `ato_mode_cmd` (se cambia desde el dashboard).
* **Suscripción del dispositivo**: define un **SUB_TOPIC** acorde a la guía de Ubidots para control por MQTT.

  > **Nota:** algunos flujos usan “control variables” y sus tópicos asociados; ajusta el SUB_TOPIC aquí y en el simulador según la doc vigente.
