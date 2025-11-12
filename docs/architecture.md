# Arquitectura (software-first)

**Principios**
- Cloud-first + **offline-safe**: reglas críticas en el nodo (ESP32/ESPHome).
- **MQTT** como columna vertebral (pub/sub eficiente).
- **TLS 8883** y token como usuario para el broker de Ubidots.

## Capas
- **Dispositivo (ESP32 + ESPHome)**: lee sensores, aplica reglas locales (ATO/umbrales), publica/escucha MQTT.
- **Nube (Ubidots)**: broker MQTT + device/variables + dashboards + alerts + (opcional) control (downlink).
- **Soporte (Tailscale)**: acceso remoto seguro sólo para mantenimiento.

## Diagrama
```mermaid
flowchart LR
  subgraph Device[Dispositivo (futuro ESP32 + ESPHome)]
    S1[pH] --> N[ESPHome Node]
    S2[Temp] --> N
    S3[Nivel low/high] --> N
    N -->|Reglas locales ATO/umbrales| A[Actuadores (bomba ATO)]
  end

  N -- MQTT TLS 8883 --> B[(Ubidots MQTT Broker)]
  B --> D[Device aquarium_iteration_01]
  D --> DB[Dashboards & Alerts]
  DB -->|cmd_ato (downlink)| B --> N

  subgraph Support[Soporte/Mantenimiento]
    T[Tailscale VPN]
  end
  T -. acceso seguro .- N
```
