# ADR-0001 — Cloud-first con Ubidots + MQTT

## Decisión
- Usar **Ubidots** como broker MQTT + backend (dashboards y alertas).
- Conexión **TLS (8883)** con **token** como usuario.
- Publicación **v2.0** a `/v2.0/devices/<device_label>` con múltiples variables y timestamp global.
- Lógica crítica **local** en el nodo (ESPHome) para operar aun sin Internet.
- **Tailscale** para mantenimiento remoto (no parte del runtime).

## Rationale
- Reduce “devops” propio, acelera el time-to-value y mantiene flexibilidad para crecer.
- MQTT es estándar IoT y eficiente; Ubidots provee path a control (downlink) y a funciones (transformaciones).

## Consecuencias
- Evitamos 24/7 en PC; el nodo funciona solo.
- Para downlink, se define una **variable de control** y se ajusta el tópico de suscripción conforme a la doc de Ubidots.
