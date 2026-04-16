<div align="center">

# Andorra Meteo <br> Home Assistant Integration

<img src="brands/logo@2x.png" width="450"/>

![Version](https://img.shields.io/badge/version-1.5.24-blue?style=for-the-badge)
![HA](https://img.shields.io/badge/Home%20Assistant-2024.1+-orange?style=for-the-badge&logo=home-assistant)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python)
![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/janfajessen)
[![Patreon](https://img.shields.io/badge/Patreon-Support-red?style=for-the-badge&logo=patreon)](https://www.patreon.com/janfajessen)
<!--[![Ko-Fi](https://img.shields.io/badge/Ko--Fi-Support-teal?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/janfajessen)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Support-pink?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/janfajessen)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue?style=for-the-badge&logo=paypal)](https://paypal.me/janfajessen)-->

**Dades meteorològiques en temps real de totes les parròquies · Butlletí d'allaus oficial**

*Fonts: [Meteoclimatic](https://www.meteoclimatic.net/) · [Servei Meteorològic Nacional d'Andorra](https://www.meteo.ad/)*

</div>

---

<details>
<summary>🇪🇸 Español</summary>

## ✨ Características

- 🌡️ **14 sensores meteorológicos** por estación — temperatura, humedad, presión, viento, precipitación y más
- 🌤️ **Entidad Weather** con icono de condición en tiempo real (sol, luna, niebla, nieve, lluvia...)
- 🏔️ **Boletín de aludes oficial** del Servicio Meteorológico Nacional — nivel de peligro por zona Norte/Centro/Sur
- ❄️ **Sensores de tipo de nieve** por zona — nieve ventada, nieve húmeda, nieve nueva...
- 🔔 **Binary sensor de aviso de aludes** — se activa cuando cualquier zona alcanza nivel ≥ 3
- 📡 **Detección automática** de nuevas estaciones — notificación a HA si aparece una estación nueva en el Principado
- 🛡️ **Datos en caché** — si una estación queda offline, conserva el último valor conocido
- 🌍 **Multilingüe** — catalán (principal), español, francés, inglés y portugués

---

## 📦 Instalación

### Vía HACS (recomendado)

1. Abre **HACS → Integraciones → ⋮ → Repositorios personalizados**
2. Añade `https://github.com/janfajessen/andorra_meteo` como tipo **Integration**
3. Busca **Andorra Meteo** e instala
4. Reinicia Home Assistant
<img src="brands/icon@2x.png" width="100"/>

### Manual

1. Copia la carpeta `custom_components/meteo_andorra/` a `config/custom_components/`
2. Reinicia Home Assistant

---

## ⚙️ Configuración

Ve a **Configuración → Dispositivos y servicios → + Añadir integración** y busca **Andorra Meteo**.

Un único desplegable donde eliges parroquia o boletín de aludes:

Canillo
Encamp
Ordino
Sant Julià de Lòria
Escaldes-Engordany
──────────────────────────────
Boletín de aludes — Principado de Andorra


> **Escaldes-Engordany** tiene dos estaciones disponibles (Centre y Sa Calma) y pedirá una segunda elección.
> Puedes añadir **múltiples estaciones**. El boletín de aludes solo se puede añadir **una vez**.

### Estaciones disponibles

| Parroquia | Estación | Altitud |
|---|---|---|
| Canillo | Els Plans de Canillo | 1.780 m |
| Encamp | Encamp | 1.270 m |
| Ordino | La Cortinada | 1.330 m |
| Sant Julià de Lòria | Certés | 1.350 m |
| Escaldes-Engordany | Centre | 1.050 m |
| Escaldes-Engordany | Sa Calma | 1.180 m |

---

## 📊 Entidades

### Estación meteorológica

| Sensor | Unidad | Descripción |
|---|---|---|
| Temperatura | °C | Temperatura actual |
| Temperatura máxima diaria | °C | Máxima del día |
| Temperatura mínima diaria | °C | Mínima del día |
| Humedad | % | Humedad actual |
| Humedad máxima / mínima diaria | % | Extremos del día |
| Presión | hPa | Presión actual |
| Presión máxima / mínima diaria | hPa | Extremos del día |
| Velocidad del viento | km/h | Viento actual |
| Racha máxima diaria | km/h | Ráfaga máxima |
| Dirección del viento | N/NE/E... | Rosa de 8 puntos cardinales |
| Orientación del viento | ° | Grados (0–360°) |
| Precipitación diaria | mm | Acumulado del día |
| Última actualización | — | Timestamp de los últimos datos reales |
| **Tiempo** | — | Weather entity con icono de condición |

### Boletín de aludes

| Sensor | Tipo | Descripción |
|---|---|---|
| Nivel de peligro — Norte | sensor | 0–5 · Ordino, Canillo (Arcalís, Grandvalira norte) |
| Nivel de peligro — Centro | sensor | 0–5 · Encamp, Escaldes (Grandvalira central, Pas de la Casa) |
| Nivel de peligro — Sur | sensor | 0–5 · Sant Julià de Lòria, Andorra la Vella |
| Tipo de nieve — Norte | sensor | Nieve ventada, Nieve húmeda, Nieve nueva... |
| Tipo de nieve — Centro | sensor | Tipo de problema por zona |
| Tipo de nieve — Sur | sensor | Tipo de problema por zona |
| Boletín válido hasta | sensor | Fecha de caducidad del boletín |
| **Aviso de aludes activo** | binary_sensor | `on` si cualquier zona ≥ 3 (Marcado) |

#### Escala europea de peligro de aludes

| Nivel | Nombre | Color |
|---|---|---|
| 0 | Sin peligro | ⬜ |
| 1 | Débil | 🟩 |
| 2 | Limitado | 🟨 |
| 3 | Marcado | 🟧 |
| 4 | Fuerte | 🟥 |
| 5 | Muy fuerte | 🟫 |

---

## 🎨 Tarjetas de ejemplo para el Dashboard

### Tarjeta meteorológica completa

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.encamp_encamp
    forecast_type: daily
  - type: glance
    title: Encamp — 1.270 m
    entities:
      - entity: sensor.encamp_encamp_temperature
        name: Temperatura
      - entity: sensor.encamp_encamp_humidity
        name: Humedad
      - entity: sensor.encamp_encamp_pressure
        name: Presión
      - entity: sensor.encamp_encamp_wind_speed
        name: Viento
      - entity: sensor.encamp_encamp_wind_direction
        name: Dirección
      - entity: sensor.encamp_encamp_daily_precipitation
        name: Precipitación
```
---

###Tarjeta de aludes con colores de nivel

```yaml
type: entities
title: 🏔️ Butlletí d'allaus — Principat d'Andorra
entities:
  - entity: binary_sensor.avis_allaus_actiu
    name: Aviso activo
  - entity: sensor.nivell_de_perill_allaus_nord
    name: Zona Norte
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_centre
    name: Zona Centro
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_sud
    name: Zona Sur
    icon: mdi:landslide-outline
  - type: divider
  - entity: sensor.tipus_de_neu_zona_nord
    name: Tipo de nieve Norte
  - entity: sensor.tipus_de_neu_zona_centre
    name: Tipo de nieve Centro
  - entity: sensor.tipus_de_neu_zona_sud
    name: Tipo de nieve Sur
  - type: divider
  - entity: sensor.butlleti_valid_fins
    name: Válido hasta
```
---

###Tarjeta de aludes con badge de colores (Mushroom Cards)

```yaml
type: horizontal-stack
cards:
  - type: custom:mushroom-template-card
    primary: Zona Norte
    secondary: "{{ states('sensor.nivell_de_perill_allaus_nord') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_nord') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zona Centro
    secondary: "{{ states('sensor.nivell_de_perill_allaus_centre') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_centre') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zona Sur
    secondary: "{{ states('sensor.nivell_de_perill_allaus_sud') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_sud') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
```
---

###Comparativa de todas las estaciones (Statistics Graph)

```yaml
type: statistics-graph
title: Temperaturas — Todas las estaciones
entities:
  - sensor.encamp_encamp_temperature
  - sensor.els_plans_de_canillo_canillo_temperature
  - sensor.la_cortinada_ordino_temperature
  - sensor.certes_sant_julia_de_loria_temperature
  - sensor.escaldes_engordany_centre_escaldes_engordany_temperature
  - sensor.escaldes_engordany_sa_calma_escaldes_engordany_temperature
stat_types:
  - mean
  - min
  - max
days_to_show: 7
```
---

##🤖 Automatizaciones de ejemplo
###Aviso por Telegram cuando el peligro de aludes es alto

```yaml
automation:
  - alias: "🏔️ Aviso peligro aludes Andorra"
    description: "Notificación cuando cualquier zona alcanza peligro marcado o superior"
    trigger:
      - platform: state
        entity_id: binary_sensor.avis_allaus_actiu
        to: "on"
    condition:
      - condition: template
        value_template: >
          {{ now().hour >= 7 and now().hour <= 22 }}
    action:
      - service: notify.telegram_jan
        data:
          message: >
            ⛷️ *AVISO DE ALUDES ACTIVO en el Principado de Andorra*

            🔴 Norte: {{ states('sensor.nivell_de_perill_allaus_nord') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_nord') }}

            🔴 Centro: {{ states('sensor.nivell_de_perill_allaus_centre') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_centre') }}

            🔴 Sur: {{ states('sensor.nivell_de_perill_allaus_sud') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}

            📅 Válido hasta: {{ states('sensor.butlleti_valid_fins') }}
            🔗 [Boletín completo](https://www.meteo.ad/neu)
```

###Aviso cuando la estación lleva más de 1 hora sin actualizar

```yaml
automation:
  - alias: "📡 Estación Encamp offline"
    trigger:
      - platform: template
        value_template: >
          {% set last = states('sensor.encamp_encamp_ultima_actualitzacio') %}
          {% if last not in ['unknown','unavailable'] %}
            {% set dt = strptime(last, '%d/%m/%Y %H:%M UTC') %}
            {{ (now().utctimetuple() | list | sum) - (dt.utctimetuple() | list | sum) > 3600 }}
          {% else %}
            false
          {% endif %}
        for: "00:05:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            📡 La estación de Encamp no ha actualizado datos en más de 1 hora.
            Última actualización: {{ states('sensor.encamp_encamp_ultima_actualitzacio') }}
```

###Aviso de helada matinal

```yaml
automation:
  - alias: "🌡️ Aviso de helada — Encamp"
    trigger:
      - platform: numeric_state
        entity_id: sensor.encamp_encamp_temperature
        below: 0
    condition:
      - condition: time
        after: "06:00:00"
        before: "10:00:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            🌡️ Temperatura bajo cero en Encamp!
            Temperatura actual: {{ states('sensor.encamp_encamp_temperature') }}°C
            Mínima del día: {{ states('sensor.encamp_encamp_daily_min_temperature') }}°C
```
---

###Notificación de nueva estación detectada

Esta automatización es automática — la integración ya crea una notificación persistente en HA
si detecta un código de estación nuevo en el Principado. No es necesario configurar nada adicional.

##🔄 Añadir una nueva estación (cuando aparezca una nueva en el Principado)
Si recibes una notificación de nueva estación detectada, el proceso es muy sencillo:

Comprueba el código nuevo en https://www.meteoclimatic.net/mapinfo/ADAND

Edita solo custom_components/meteo_andorra/const.py añadiendo la estación al bloque PARISHES

Reinicia Home Assistant

Añade la nueva instancia desde la integración

---

###📝 Notas técnicas

Polling: Estaciones cada 30 min · Boletín de aludes cada 60 min · Detección de estaciones nuevas cada 24h

Caché: Si una estación queda offline, las entidades mantienen el último valor conocido hasta recuperar conexión

Valor -99: Meteoclimatic usa -99 como indicador de sensor averiado — la integración lo filtra y muestra None

Domicilio técnico: meteo_andorra (no cambiar por compatibilidad con instalaciones existentes)


</details>

<details>
<summary>🇫🇷 Français</summary>

## ✨ Caractéristiques

- 🌡️ **14 capteurs météorologiques** par station — température, humidité, pression, vent, précipitations et plus
- 🌤️ **Entité Weather** avec icône de condition en temps réel (soleil, lune, brouillard, neige, pluie...)
- 🏔️ **Bulletin d'avalanches officiel** du Service Météorologique National — niveau de danger par zone Nord/Centre/Sud
- ❄️ **Capteurs de type de neige** par zone — neige soufflée, neige humide, neige fraîche...
- 🔔 **Binary sensor d'alerte avalanches** — s'active quand une zone atteint un niveau ≥ 3
- 📡 **Détection automatique** des nouvelles stations — notification à HA si une nouvelle station apparaît dans la Principauté
- 🛡️ **Données en cache** — si une station est hors ligne, conserve la dernière valeur connue
- 🌍 **Multilingue** — catalan (principal), espagnol, français, anglais et portugais

---

## 📦 Installation

### Via HACS (recommandé)

1. Ouvrez **HACS → Intégrations → ⋮ → Dépôts personnalisés**
2. Ajoutez `https://github.com/janfajessen/andorra_meteo` comme type **Integration**
3. Cherchez **Andorra Meteo** et installez
4. Redémarrez Home Assistant
<img src="brands/icon@2x.png" width="100"/>

### Manuellement

1. Copiez le dossier `custom_components/meteo_andorra/` vers `config/custom_components/`
2. Redémarrez Home Assistant

---

## ⚙️ Configuration

Allez dans **Configuration → Appareils et services → + Ajouter une intégration** et cherchez **Andorra Meteo**.

Une seule liste déroulante où vous choisissez la paroisse ou le bulletin d'avalanches :

Canillo
Encamp
Ordino
Sant Julià de Lòria
Escaldes-Engordany
──────────────────────────────
Butlletí d'allaus — Principat d'Andorra


> **Escaldes-Engordany** dispose de deux stations disponibles (Centre et Sa Calma) et demandera un second choix.
> Vous pouvez ajouter **plusieurs stations**. Le bulletin d'avalanches ne peut être ajouté **qu'une seule fois**.

### Stations disponibles

| Paroisse | Station | Altitude |
|---|---|---|
| Canillo | Els Plans de Canillo | 1.780 m |
| Encamp | Encamp | 1.270 m |
| Ordino | La Cortinada | 1.330 m |
| Sant Julià de Lòria | Certés | 1.350 m |
| Escaldes-Engordany | Centre | 1.050 m |
| Escaldes-Engordany | Sa Calma | 1.180 m |

---

## 📊 Entités

### Station météorologique

| Capteur | Unité | Description |
|---|---|---|
| Température | °C | Température actuelle |
| Température maximale journalière | °C | Maximale du jour |
| Température minimale journalière | °C | Minimale du jour |
| Humidité | % | Humidité actuelle |
| Humidité maximale / minimale journalière | % | Extrêmes du jour |
| Pression | hPa | Pression actuelle |
| Pression maximale / minimale journalière | hPa | Extrêmes du jour |
| Vitesse du vent | km/h | Vent actuel |
| Rafale maximale journalière | km/h | Rafale maximale |
| Direction du vent | N/NE/E... | Rose des 8 points cardinaux |
| Orientation du vent | ° | Degrés (0–360°) |
| Précipitation journalière | mm | Cumul du jour |
| Dernière mise à jour | — | Horodatage des dernières données réelles |
| **Temps** | — | Entité Weather avec icône de condition |

### Bulletin d'avalanches

| Capteur | Type | Description |
|---|---|---|
| Niveau de danger — Nord | sensor | 0–5 · Ordino, Canillo (Arcalís, Grandvalira nord) |
| Niveau de danger — Centre | sensor | 0–5 · Encamp, Escaldes (Grandvalira central, Pas de la Casa) |
| Niveau de danger — Sud | sensor | 0–5 · Sant Julià de Lòria, Andorra la Vella |
| Type de neige — Nord | sensor | Neige soufflée, Neige humide, Neige fraîche... |
| Type de neige — Centre | sensor | Type de problème par zone |
| Type de neige — Sud | sensor | Type de problème par zone |
| Bulletin valable jusqu'au | sensor | Date d'expiration du bulletin |
| **Alerte avalanche active** | binary_sensor | `on` si une zone ≥ 3 (Marqué) |

#### Échelle européenne du danger d'avalanches

| Niveau | Nom |
|---|---|---|
| 0 | Pas de danger |
| 1 | Faible |
| 2 | Limité | 
| 3 | Marqué | 
| 4 | Fort | 
| 5 | Très fort |

---

## 🎨 Cartes d'exemple pour le Dashboard

### Carte météo complète

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.encamp_encamp
    forecast_type: daily
  - type: glance
    title: Encamp — 1.270 m
    entities:
      - entity: sensor.encamp_encamp_temperature
        name: Température
      - entity: sensor.encamp_encamp_humidity
        name: Humidité
      - entity: sensor.encamp_encamp_pressure
        name: Pression
      - entity: sensor.encamp_encamp_wind_speed
        name: Vent
      - entity: sensor.encamp_encamp_wind_direction
        name: Direction
      - entity: sensor.encamp_encamp_daily_precipitation
        name: Précipitation
```

###Carte avalanches avec couleurs de niveau

```yaml
type: entities
title: 🏔️ Butlletí d'allaus — Principat d'Andorra
entities:
  - entity: binary_sensor.avis_allaus_actiu
    name: Alerte active
  - entity: sensor.nivell_de_perill_allaus_nord
    name: Zone Nord
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_centre
    name: Zone Centre
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_sud
    name: Zone Sud
    icon: mdi:landslide-outline
  - type: divider
  - entity: sensor.tipus_de_neu_zona_nord
    name: Type de neige Nord
  - entity: sensor.tipus_de_neu_zona_centre
    name: Type de neige Centre
  - entity: sensor.tipus_de_neu_zona_sud
    name: Type de neige Sud
  - type: divider
  - entity: sensor.butlleti_valid_fins
    name: Valable jusqu'au
```

###Carte avalanches avec badge de couleurs (Mushroom Cards)

```yaml
type: horizontal-stack
cards:
  - type: custom:mushroom-template-card
    primary: Zone Nord
    secondary: "{{ states('sensor.nivell_de_perill_allaus_nord') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_nord') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zone Centre
    secondary: "{{ states('sensor.nivell_de_perill_allaus_centre') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_centre') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zone Sud
    secondary: "{{ states('sensor.nivell_de_perill_allaus_sud') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_sud') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
```

###Comparaison de toutes les stations (Statistics Graph)

```yaml
type: statistics-graph
title: Températures — Toutes les stations
entities:
  - sensor.encamp_encamp_temperature
  - sensor.els_plans_de_canillo_canillo_temperature
  - sensor.la_cortinada_ordino_temperature
  - sensor.certes_sant_julia_de_loria_temperature
  - sensor.escaldes_engordany_centre_escaldes_engordany_temperature
  - sensor.escaldes_engordany_sa_calma_escaldes_engordany_temperature
stat_types:
  - mean
  - min
  - max
days_to_show: 7
```

##🤖 Automatisations d'exemple
###Alerte par Telegram quand le danger d'avalanches est élevé

```yaml
automation:
  - alias: "🏔️ Alerte danger avalanches Andorre"
    description: "Notification quand une zone atteint un danger marqué ou supérieur"
    trigger:
      - platform: state
        entity_id: binary_sensor.avis_allaus_actiu
        to: "on"
    condition:
      - condition: template
        value_template: >
          {{ now().hour >= 7 and now().hour <= 22 }}
    action:
      - service: notify.telegram_jan
        data:
          message: >
            ⛷️ *ALERTE AVALANCHE ACTIVE dans la Principauté d'Andorre*

            🔴 Nord: {{ states('sensor.nivell_de_perill_allaus_nord') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_nord') }}

            🔴 Centre: {{ states('sensor.nivell_de_perill_allaus_centre') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_centre') }}

            🔴 Sud: {{ states('sensor.nivell_de_perill_allaus_sud') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}

            📅 Valable jusqu'au: {{ states('sensor.butlleti_valid_fins') }}
            🔗 [Bulletin complet](https://www.meteo.ad/neu)
```

###Alerte quand la station n'a pas mis à jour depuis plus d'1 heure

```yaml
automation:
  - alias: "📡 Station Encamp hors ligne"
    trigger:
      - platform: template
        value_template: >
          {% set last = states('sensor.encamp_encamp_ultima_actualitzacio') %}
          {% if last not in ['unknown','unavailable'] %}
            {% set dt = strptime(last, '%d/%m/%Y %H:%M UTC') %}
            {{ (now().utctimetuple() | list | sum) - (dt.utctimetuple() | list | sum) > 3600 }}
          {% else %}
            false
          {% endif %}
        for: "00:05:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            📡 La station d'Encamp n'a pas mis à jour ses données depuis plus d'1 heure.
            Dernière mise à jour: {{ states('sensor.encamp_encamp_ultima_actualitzacio') }}
```

###Alerte de gel matinal

```yaml
automation:
  - alias: "🌡️ Alerte de gel — Encamp"
    trigger:
      - platform: numeric_state
        entity_id: sensor.encamp_encamp_temperature
        below: 0
    condition:
      - condition: time
        after: "06:00:00"
        before: "10:00:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            🌡️ Température en dessous de zéro à Encamp !
            Température actuelle: {{ states('sensor.encamp_encamp_temperature') }}°C
            Minimale du jour: {{ states('sensor.encamp_encamp_daily_min_temperature') }}°C
```
###Notification de nouvelle station détectée

Cette automatisation est automatique — l'intégration crée déjà une notification persistante dans HA
si elle détecte un nouveau code de station dans la Principauté. Aucune configuration supplémentaire nécessaire.

##🔄 Ajouter une nouvelle station (quand une nouvelle apparaît dans la Principauté)
Si vous recevez une notification de nouvelle station détectée, le processus est très simple :

Vérifiez le nouveau code sur https://www.meteoclimatic.net/mapinfo/ADAND

Éditez seulement custom_components/meteo_andorra/const.py en ajoutant la station au bloc PARISHES

Redémarrez Home Assistant

Ajoutez la nouvelle instance depuis l'intégration

---

###📝 Notes techniques

Polling: Stations toutes les 30 min · Bulletin d'avalanches toutes les 60 min · Détection de nouvelles stations toutes les 24h

Cache: Si une station est hors ligne, les entités conservent la dernière valeur connue jusqu'à rétablissement de la connexion

Valeur -99: Meteoclimatic utilise -99 comme indicateur de capteur défectueux — l'intégration le filtre et affiche None

Domicile technique: meteo_andorra (ne pas changer pour compatibilité avec les installations existantes)

</details>

<details>
<summary>🇬🇧 English</summary>

## ✨ Features

- 🌡️ **14 weather sensors** per station — temperature, humidity, pressure, wind, precipitation and more
- 🌤️ **Weather entity** with real-time condition icon (sun, moon, fog, snow, rain...)
- 🏔️ **Official avalanche bulletin** from the National Weather Service — danger level for North/Center/South zones
- ❄️ **Snow type sensors** per zone — wind-blown snow, wet snow, fresh snow...
- 🔔 **Avalanche warning binary sensor** — activates when any zone reaches level ≥ 3
- 📡 **Automatic detection** of new stations — notification to HA if a new station appears in the Principality
- 🛡️ **Cached data** — if a station goes offline, keeps the last known value
- 🌍 **Multilingual** — Catalan (primary), Spanish, French, English and Portuguese

---

## 📦 Installation

### Via HACS (recommended)

1. Open **HACS → Integrations → ⋮ → Custom repositories**
2. Add `https://github.com/janfajessen/andorra_meteo` as type **Integration**
3. Search for **Andorra Meteo** and install
4. Restart Home Assistant
<img src="brands/icon@2x.png" width="100"/>

### Manual

1. Copy the `custom_components/meteo_andorra/` folder to `config/custom_components/`
2. Restart Home Assistant

---

## ⚙️ Configuration

Go to **Configuration → Devices & Services → + Add integration** and search for **Andorra Meteo**.

A single dropdown where you choose parish or avalanche bulletin:

Canillo
Encamp
Ordino
Sant Julià de Lòria
Escaldes-Engordany
──────────────────────────────
Butlletí d'allaus — Principat d'Andorra


> **Escaldes-Engordany** has two stations available (Centre and Sa Calma) and will ask for a second choice.
> You can add **multiple stations**. The avalanche bulletin can only be added **once**.

### Available stations

| Parish | Station | Altitude |
|---|---|---|
| Canillo | Els Plans de Canillo | 1,780 m |
| Encamp | Encamp | 1,270 m |
| Ordino | La Cortinada | 1,330 m |
| Sant Julià de Lòria | Certés | 1,350 m |
| Escaldes-Engordany | Centre | 1,050 m |
| Escaldes-Engordany | Sa Calma | 1,180 m |

---

## 📊 Entities

### Weather station

| Sensor | Unit | Description |
|---|---|---|
| Temperature | °C | Current temperature |
| Daily maximum temperature | °C | Day's maximum |
| Daily minimum temperature | °C | Day's minimum |
| Humidity | % | Current humidity |
| Daily max / min humidity | % | Day's extremes |
| Pressure | hPa | Current pressure |
| Daily max / min pressure | hPa | Day's extremes |
| Wind speed | km/h | Current wind |
| Daily maximum gust | km/h | Maximum gust |
| Wind direction | N/NE/E... | 8-point compass rose |
| Wind bearing | ° | Degrees (0–360°) |
| Daily precipitation | mm | Day's accumulation |
| Last update | — | Timestamp of last real data |
| **Weather** | — | Weather entity with condition icon |

### Avalanche bulletin

| Sensor | Type | Description |
|---|---|---|
| Danger level — North | sensor | 0–5 · Ordino, Canillo (Arcalís, Grandvalira north) |
| Danger level — Center | sensor | 0–5 · Encamp, Escaldes (Grandvalira central, Pas de la Casa) |
| Danger level — South | sensor | 0–5 · Sant Julià de Lòria, Andorra la Vella |
| Snow type — North | sensor | Wind-blown snow, Wet snow, Fresh snow... |
| Snow type — Center | sensor | Problem type per zone |
| Snow type — South | sensor | Problem type per zone |
| Bulletin valid until | sensor | Bulletin expiry date |
| **Avalanche warning active** | binary_sensor | `on` if any zone ≥ 3 (Considerable) |

#### European avalanche danger scale

| Level | Name | Color |
|---|---|---|
| 0 | No danger | ⬜ |
| 1 | Low | 🟩 |
| 2 | Limited | 🟨 |
| 3 | Considerable | 🟧 |
| 4 | High | 🟥 |
| 5 | Very high | 🟫 |

---

## 🎨 Example dashboard cards

### Complete weather card

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.encamp_encamp
    forecast_type: daily
  - type: glance
    title: Encamp — 1,270 m
    entities:
      - entity: sensor.encamp_encamp_temperature
        name: Temperature
      - entity: sensor.encamp_encamp_humidity
        name: Humidity
      - entity: sensor.encamp_encamp_pressure
        name: Pressure
      - entity: sensor.encamp_encamp_wind_speed
        name: Wind
      - entity: sensor.encamp_encamp_wind_direction
        name: Direction
      - entity: sensor.encamp_encamp_daily_precipitation
        name: Precipitation
```

###Avalanche card with level colors

```yaml
type: entities
title: 🏔️ Butlletí d'allaus — Principat d'Andorra
entities:
  - entity: binary_sensor.avis_allaus_actiu
    name: Active warning
  - entity: sensor.nivell_de_perill_allaus_nord
    name: North Zone
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_centre
    name: Center Zone
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_sud
    name: South Zone
    icon: mdi:landslide-outline
  - type: divider
  - entity: sensor.tipus_de_neu_zona_nord
    name: Snow type North
  - entity: sensor.tipus_de_neu_zona_centre
    name: Snow type Center
  - entity: sensor.tipus_de_neu_zona_sud
    name: Snow type South
  - type: divider
  - entity: sensor.butlleti_valid_fins
    name: Valid until
```

###Avalanche card with color badges (Mushroom Cards)

```yaml
type: horizontal-stack
cards:
  - type: custom:mushroom-template-card
    primary: North Zone
    secondary: "{{ states('sensor.nivell_de_perill_allaus_nord') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_nord') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Center Zone
    secondary: "{{ states('sensor.nivell_de_perill_allaus_centre') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_centre') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: South Zone
    secondary: "{{ states('sensor.nivell_de_perill_allaus_sud') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_sud') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
```

###All stations comparison (Statistics Graph)

```yaml
type: statistics-graph
title: Temperatures — All stations
entities:
  - sensor.encamp_encamp_temperature
  - sensor.els_plans_de_canillo_canillo_temperature
  - sensor.la_cortinada_ordino_temperature
  - sensor.certes_sant_julia_de_loria_temperature
  - sensor.escaldes_engordany_centre_escaldes_engordany_temperature
  - sensor.escaldes_engordany_sa_calma_escaldes_engordany_temperature
stat_types:
  - mean
  - min
  - max
days_to_show: 7
```

##🤖 Example automations
###Telegram alert when avalanche danger is high

```yaml
automation:
  - alias: "🏔️ Andorra avalanche danger alert"
    description: "Notification when any zone reaches considerable danger or higher"
    trigger:
      - platform: state
        entity_id: binary_sensor.avis_allaus_actiu
        to: "on"
    condition:
      - condition: template
        value_template: >
          {{ now().hour >= 7 and now().hour <= 22 }}
    action:
      - service: notify.telegram_jan
        data:
          message: >
            ⛷️ *AVALANCHE WARNING ACTIVE in the Principality of Andorra*

            🔴 North: {{ states('sensor.nivell_de_perill_allaus_nord') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_nord') }}

            🔴 Center: {{ states('sensor.nivell_de_perill_allaus_centre') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_centre') }}

            🔴 South: {{ states('sensor.nivell_de_perill_allaus_sud') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}

            📅 Valid until: {{ states('sensor.butlleti_valid_fins') }}
            🔗 [Full bulletin](https://www.meteo.ad/neu)
```

###Alert when station has been offline for more than 1 hour

```yaml
automation:
  - alias: "📡 Encamp station offline"
    trigger:
      - platform: template
        value_template: >
          {% set last = states('sensor.encamp_encamp_ultima_actualitzacio') %}
          {% if last not in ['unknown','unavailable'] %}
            {% set dt = strptime(last, '%d/%m/%Y %H:%M UTC') %}
            {{ (now().utctimetuple() | list | sum) - (dt.utctimetuple() | list | sum) > 3600 }}
          {% else %}
            false
          {% endif %}
        for: "00:05:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            📡 The Encamp station has not updated data for more than 1 hour.
            Last update: {{ states('sensor.encamp_encamp_ultima_actualitzacio') }}
```

###Morning frost alert

```yaml
automation:
  - alias: "🌡️ Frost alert — Encamp"
    trigger:
      - platform: numeric_state
        entity_id: sensor.encamp_encamp_temperature
        below: 0
    condition:
      - condition: time
        after: "06:00:00"
        before: "10:00:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            🌡️ Below zero temperature in Encamp!
            Current temperature: {{ states('sensor.encamp_encamp_temperature') }}°C
            Day's minimum: {{ states('sensor.encamp_encamp_daily_min_temperature') }}°C
```
---

###New station detected notification
This automation is automatic — the integration already creates a persistent notification in HA
if it detects a new station code in the Principality. No additional configuration needed.

###🔄 Adding a new station (when a new one appears in the Principality)
If you receive a new station detected notification, the process is very simple:

Check the new code at https://www.meteoclimatic.net/mapinfo/ADAND

Edit only custom_components/meteo_andorra/const.py adding the station to the PARISHES block

Restart Home Assistant

Add the new instance from the integration

---

##📝 Technical notes
Polling: Stations every 30 min · Avalanche bulletin every 60 min · New station detection every 24h

Cache: If a station goes offline, entities keep the last known value until connection is restored

Value -99: Meteoclimatic uses -99 as a faulty sensor indicator — the integration filters it and shows None

Technical name: meteo_andorra (do not change for compatibility with existing installations)

</details>



<details>
<summary>🇵🇹 Português</summary>

## ✨ Características

- 🌡️ **14 sensores meteorológicos** por estação — temperatura, humidade, pressão, vento, precipitação e mais
- 🌤️ **Entidade Weather** com ícone de condição em tempo real (sol, lua, nevoeiro, neve, chuva...)
- 🏔️ **Boletim de avalanches oficial** do Serviço Meteorológico Nacional — nível de perigo por zona Norte/Centro/Sul
- ❄️ **Sensores de tipo de neve** por zona — neve soprada, neve húmida, neve nova...
- 🔔 **Binary sensor de aviso de avalanches** — ativa quando qualquer zona atinge nível ≥ 3
- 📡 **Deteção automática** de novas estações — notificação para HA se aparecer uma estação nova no Principado
- 🛡️ **Dados em cache** — se uma estação ficar offline, mantém o último valor conhecido
- 🌍 **Multilingue** — catalão (principal), espanhol, francês, inglês e português

---

## 📦 Instalação

### Via HACS (recomendado)

1. Abra **HACS → Integrações → ⋮ → Repositórios personalizados**
2. Adicione `https://github.com/janfajessen/andorra_meteo` como tipo **Integration**
3. Procure por **Andorra Meteo** e instale
4. Reinicie o Home Assistant
<img src="brands/icon@2x.png" width="100"/>

### Manual

1. Copie a pasta `custom_components/meteo_andorra/` para `config/custom_components/`
2. Reinicie o Home Assistant

---

## ⚙️ Configuração

Vá a **Configuração → Dispositivos e serviços → + Adicionar integração** e procure por **Andorra Meteo**.

Uma única lista suspensa onde escolhe a freguesia ou boletim de avalanches:

Canillo
Encamp
Ordino
Sant Julià de Lòria
Escaldes-Engordany
──────────────────────────────
Butlletí d'allaus — Principat d'Andorra


> **Escaldes-Engordany** tem duas estações disponíveis (Centre e Sa Calma) e pedirá uma segunda escolha.
> Pode adicionar **múltiplas estações**. O boletim de avalanches só pode ser adicionado **uma vez**.

### Estações disponíveis

| Freguesia | Estação | Altitude |
|---|---|---|
| Canillo | Els Plans de Canillo | 1.780 m |
| Encamp | Encamp | 1.270 m |
| Ordino | La Cortinada | 1.330 m |
| Sant Julià de Lòria | Certés | 1.350 m |
| Escaldes-Engordany | Centre | 1.050 m |
| Escaldes-Engordany | Sa Calma | 1.180 m |

---

## 📊 Entidades

### Estação meteorológica

| Sensor | Unidade | Descrição |
|---|---|---|
| Temperatura | °C | Temperatura atual |
| Temperatura máxima diária | °C | Máxima do dia |
| Temperatura mínima diária | °C | Mínima do dia |
| Humidade | % | Humidade atual |
| Humidade máxima / mínima diária | % | Extremos do dia |
| Pressão | hPa | Pressão atual |
| Pressão máxima / mínima diária | hPa | Extremos do dia |
| Velocidade do vento | km/h | Vento atual |
| Rajada máxima diária | km/h | Rajada máxima |
| Direção do vento | N/NE/E... | Rosa dos 8 pontos cardeais |
| Orientação do vento | ° | Graus (0–360°) |
| Precipitação diária | mm | Acumulado do dia |
| Última atualização | — | Timestamp dos últimos dados reais |
| **Tempo** | — | Weather entity com ícone de condição |

### Boletim de avalanches

| Sensor | Tipo | Descrição |
|---|---|---|
| Nível de perigo — Norte | sensor | 0–5 · Ordino, Canillo (Arcalís, Grandvalira norte) |
| Nível de perigo — Centro | sensor | 0–5 · Encamp, Escaldes (Grandvalira central, Pas de la Casa) |
| Nível de perigo — Sul | sensor | 0–5 · Sant Julià de Lòria, Andorra la Vella |
| Tipo de neve — Norte | sensor | Neve soprada, Neve húmida, Neve nova... |
| Tipo de neve — Centro | sensor | Tipo de problema por zona |
| Tipo de neve — Sul | sensor | Tipo de problema por zona |
| Boletim válido até | sensor | Data de expiração do boletim |
| **Aviso de avalanches ativo** | binary_sensor | `on` se qualquer zona ≥ 3 (Marcado) |

#### Escala europeia de perigo de avalanches

| Nível | Nome | Cor |
|---|---|---|
| 0 | Sem perigo | ⬜ |
| 1 | Fraco | 🟩 |
| 2 | Limitado | 🟨 |
| 3 | Marcado | 🟧 |
| 4 | Forte | 🟥 |
| 5 | Muito forte | 🟫 |

---

## 🎨 Exemplos de cartões para o Dashboard

### Cartão meteorológico completo

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.encamp_encamp
    forecast_type: daily
  - type: glance
    title: Encamp — 1.270 m
    entities:
      - entity: sensor.encamp_encamp_temperature
        name: Temperatura
      - entity: sensor.encamp_encamp_humidity
        name: Humidade
      - entity: sensor.encamp_encamp_pressure
        name: Pressão
      - entity: sensor.encamp_encamp_wind_speed
        name: Vento
      - entity: sensor.encamp_encamp_wind_direction
        name: Direção
      - entity: sensor.encamp_encamp_daily_precipitation
        name: Precipitação
```

###Cartão de avalanches com cores de nível

```yaml
type: entities
title: 🏔️ Butlletí d'allaus — Principat d'Andorra
entities:
  - entity: binary_sensor.avis_allaus_actiu
    name: Aviso ativo
  - entity: sensor.nivell_de_perill_allaus_nord
    name: Zona Norte
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_centre
    name: Zona Centro
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_sud
    name: Zona Sul
    icon: mdi:landslide-outline
  - type: divider
  - entity: sensor.tipus_de_neu_zona_nord
    name: Tipo de neve Norte
  - entity: sensor.tipus_de_neu_zona_centre
    name: Tipo de neve Centro
  - entity: sensor.tipus_de_neu_zona_sud
    name: Tipo de neve Sul
  - type: divider
  - entity: sensor.butlleti_valid_fins
    name: Válido até
```

###Cartão de avalanches com badge de cores (Mushroom Cards)

```yaml
type: horizontal-stack
cards:
  - type: custom:mushroom-template-card
    primary: Zona Norte
    secondary: "{{ states('sensor.nivell_de_perill_allaus_nord') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_nord') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zona Centro
    secondary: "{{ states('sensor.nivell_de_perill_allaus_centre') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_centre') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zona Sul
    secondary: "{{ states('sensor.nivell_de_perill_allaus_sud') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_sud') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
```

###Comparação de todas as estações (Statistics Graph)

```yaml
type: statistics-graph
title: Temperaturas — Todas as estações
entities:
  - sensor.encamp_encamp_temperature
  - sensor.els_plans_de_canillo_canillo_temperature
  - sensor.la_cortinada_ordino_temperature
  - sensor.certes_sant_julia_de_loria_temperature
  - sensor.escaldes_engordany_centre_escaldes_engordany_temperature
  - sensor.escaldes_engordany_sa_calma_escaldes_engordany_temperature
stat_types:
  - mean
  - min
  - max
days_to_show: 7
```

##🤖 Automações de exemplo
###Aviso por Telegram quando o perigo de avalanches é alto

```yaml
automation:
  - alias: "🏔️ Aviso perigo avalanches Andorra"
    description: "Notificação quando qualquer zona atinge perigo marcado ou superior"
    trigger:
      - platform: state
        entity_id: binary_sensor.avis_allaus_actiu
        to: "on"
    condition:
      - condition: template
        value_template: >
          {{ now().hour >= 7 and now().hour <= 22 }}
    action:
      - service: notify.telegram_jan
        data:
          message: >
            ⛷️ *AVISO DE AVALANCHES ATIVO no Principado de Andorra*

            🔴 Norte: {{ states('sensor.nivell_de_perill_allaus_nord') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_nord') }}

            🔴 Centro: {{ states('sensor.nivell_de_perill_allaus_centre') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_centre') }}

            🔴 Sul: {{ states('sensor.nivell_de_perill_allaus_sud') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}

            📅 Válido até: {{ states('sensor.butlleti_valid_fins') }}
            🔗 [Boletim completo](https://www.meteo.ad/neu)
```

###Aviso quando a estação está há mais de 1 hora sem atualizar

```yaml
automation:
  - alias: "📡 Estação Encamp offline"
    trigger:
      - platform: template
        value_template: >
          {% set last = states('sensor.encamp_encamp_ultima_actualitzacio') %}
          {% if last not in ['unknown','unavailable'] %}
            {% set dt = strptime(last, '%d/%m/%Y %H:%M UTC') %}
            {{ (now().utctimetuple() | list | sum) - (dt.utctimetuple() | list | sum) > 3600 }}
          {% else %}
            false
          {% endif %}
        for: "00:05:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            📡 A estação de Encamp não atualizou dados há mais de 1 hora.
            Última atualização: {{ states('sensor.encamp_encamp_ultima_actualitzacio') }}
```

###Aviso de geada matinal

```yaml
automation:
  - alias: "🌡️ Aviso de geada — Encamp"
    trigger:
      - platform: numeric_state
        entity_id: sensor.encamp_encamp_temperature
        below: 0
    condition:
      - condition: time
        after: "06:00:00"
        before: "10:00:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            🌡️ Temperatura abaixo de zero em Encamp!
            Temperatura atual: {{ states('sensor.encamp_encamp_temperature') }}°C
            Mínima do dia: {{ states('sensor.encamp_encamp_daily_min_temperature') }}°C
```

---

##Notificação de nova estação detetada
Esta automação é automática — a integração já cria uma notificação persistente no HA
se detetar um novo código de estação no Principado. Não é necessário configurar nada adicional.

###🔄 Adicionar uma nova estação (quando aparecer uma nova no Principado)
Se receber uma notificação de nova estação detetada, o processo é muito simples:

Verifique o novo código em https://www.meteoclimatic.net/mapinfo/ADAND

Edite apenas custom_components/meteo_andorra/const.py adicionando a estação ao bloco PARISHES

Reinicie o Home Assistant

Adicione a nova instância a partir da integração

---

##📝 Notas técnicas
Polling: Estações a cada 30 min · Boletim de avalanches a cada 60 min · Deteção de novas estações a cada 24h

Cache: Se uma estação ficar offline, as entidades mantêm o último valor conhecido até recuperar a ligação

Valor -99: Meteoclimatic usa -99 como indicador de sensor avariado — a integração filtra e mostra None

Domínio técnico: meteo_andorra (não alterar para compatibilidade com instalações existentes)
</details>

---

## ✨ Característiques

- 🌡️ **14 sensors meteorològics** per estació — temperatura, humitat, pressió, vent, precipitació i més
- 🌤️ **Entitat Weather** amb icona de condició en temps real (sol, lluna, boira, neu, pluja...)
- 🏔️ **Butlletí d'allaus oficial** del Servei Meteorològic Nacional — nivell de perill per zona Nord/Centre/Sud
- ❄️ **Sensors de tipus de neu** per zona — neu ventada, neu humida, neu nova...
- 🔔 **Binary sensor d'avís d'allaus** — s'activa quan qualsevol zona assoleix nivell ≥ 3
- 📡 **Detecció automàtica** de noves estacions — notificació a HA si apareix una estació nova al Principat
- 🛡️ **Dades en caché** — si una estació queda offline, conserva l'últim valor conegut
- 🌍 **Multilingüe** — català (principal), espanyol, francès, anglès i portuguès

---

## 📦 Instal·lació

### Via HACS (recomanat)

1. Obre **HACS → Integracions → ⋮ → Repositoris personalitzats**
2. Afegeix `https://github.com/janfajessen/andorra_meteo` com a tipus **Integration**
3. Cerca **Andorra Meteo** i instal·la
4. Reinicia Home Assistant
<img src="brands/icon@2x.png" width="100"/>

### Manual

1. Copia la carpeta `custom_components/meteo_andorra/` a `config/custom_components/`
2. Reinicia Home Assistant

---

## ⚙️ Configuració

Ves a **Configuració → Dispositius i serveis → + Afegeix integració** i cerca **Andorra Meteo**.

Un sol desplegable on tries parròquia o butlletí d'allaus:

```
Canillo
Encamp
Ordino
Sant Julià de Lòria
Escaldes-Engordany
──────────────────────────────
Butlletí d'allaus — Principat d'Andorra
```

> **Escaldes-Engordany** té dues estacions disponibles (Centre i Sa Calma) i demanarà una segona elecció.
> Pots afegir **múltiples estacions**. El butlletí d'allaus només es pot afegir **una vegada**.

### Estacions disponibles

| Parròquia | Estació | Altitud |
|---|---|---|
| Canillo | Els Plans de Canillo | 1.780 m |
| Encamp | Encamp | 1.270 m |
| Ordino | La Cortinada | 1.330 m |
| Sant Julià de Lòria | Certés | 1.350 m |
| Escaldes-Engordany | Centre | 1.050 m |
| Escaldes-Engordany | Sa Calma | 1.180 m |

---

## 📊 Entitats

### Estació meteorològica

| Sensor | Unitat | Descripció |
|---|---|---|
| Temperatura | °C | Temperatura actual |
| Temperatura màxima diària | °C | Màxima del dia |
| Temperatura mínima diària | °C | Mínima del dia |
| Humitat | % | Humitat actual |
| Humitat màxima / mínima diària | % | Extrems del dia |
| Pressió | hPa | Pressió actual |
| Pressió màxima / mínima diària | hPa | Extrems del dia |
| Velocitat del vent | km/h | Vent actual |
| Ratxa màxima diària | km/h | Ràfega màxima |
| Direcció del vent | N/NE/E... | Rosa de 8 punts cardinals |
| Orientació del vent | ° | Graus (0–360°) |
| Precipitació diària | mm | Acumulat del dia |
| Última actualització | — | Timestamp de les últimes dades reals |
| **Temps** | — | Weather entity amb icona de condició |

### Butlletí d'allaus

| Sensor | Tipus | Descripció |
|---|---|---|
| Nivell de perill — Nord | sensor | 0–5 · Ordino, Canillo (Arcalís, Grandvalira nord) |
| Nivell de perill — Centre | sensor | 0–5 · Encamp, Escaldes (Grandvalira central, Pas de la Casa) |
| Nivell de perill — Sud | sensor | 0–5 · Sant Julià de Lòria, Andorra la Vella |
| Tipus de neu — Nord | sensor | Neu ventada, Neu humida, Neu nova... |
| Tipus de neu — Centre | sensor | Tipus de problema per zona |
| Tipus de neu — Sud | sensor | Tipus de problema per zona |
| Butlletí vàlid fins | sensor | Data de caducitat del butlletí |
| **Avís d'allaus actiu** | binary_sensor | `on` si qualsevol zona ≥ 3 (Marcat) |

#### Escala europea de perill d'allaus

| Nivell | Nom |
|---|---|---|
| 0 | Sense perill |
| 1 | Feble |
| 2 | Limitat |
| 3 | Marcat |
| 4 | Fort |
| 5 | Molt fort |

---

## 🎨 Targetes de exemple per al Dashboard

### Targeta meteorològica completa

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.encamp_encamp
    forecast_type: daily
  - type: glance
    title: Encamp — 1.270 m
    entities:
      - entity: sensor.encamp_encamp_temperature
        name: Temperatura
      - entity: sensor.encamp_encamp_humidity
        name: Humitat
      - entity: sensor.encamp_encamp_pressure
        name: Pressió
      - entity: sensor.encamp_encamp_wind_speed
        name: Vent
      - entity: sensor.encamp_encamp_wind_direction
        name: Direcció
      - entity: sensor.encamp_encamp_daily_precipitation
        name: Precipitació
```

### Targeta d'allaus amb colors de nivell

```yaml
type: entities
title: 🏔️ Butlletí d'allaus — Principat d'Andorra
entities:
  - entity: binary_sensor.avis_allaus_actiu
    name: Avís actiu
  - entity: sensor.nivell_de_perill_allaus_nord
    name: Zona Nord
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_centre
    name: Zona Centre
    icon: mdi:landslide-outline
  - entity: sensor.nivell_de_perill_allaus_sud
    name: Zona Sud
    icon: mdi:landslide-outline
  - type: divider
  - entity: sensor.tipus_de_neu_zona_nord
    name: Tipus de neu Nord
  - entity: sensor.tipus_de_neu_zona_centre
    name: Tipus de neu Centre
  - entity: sensor.tipus_de_neu_zona_sud
    name: Tipus de neu Sud
  - type: divider
  - entity: sensor.butlleti_valid_fins
    name: Vàlid fins
```

### Targeta d'allaus amb badge de colors (Mushroom Cards)

```yaml
type: horizontal-stack
cards:
  - type: custom:mushroom-template-card
    primary: Zona Nord
    secondary: "{{ states('sensor.nivell_de_perill_allaus_nord') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_nord') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zona Centre
    secondary: "{{ states('sensor.nivell_de_perill_allaus_centre') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_centre') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
  - type: custom:mushroom-template-card
    primary: Zona Sud
    secondary: "{{ states('sensor.nivell_de_perill_allaus_sud') }}/5 · {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}"
    icon: mdi:landslide-outline
    icon_color: >
      {% set n = states('sensor.nivell_de_perill_allaus_sud') | int %}
      {% if n == 0 %} grey
      {% elif n == 1 %} green
      {% elif n == 2 %} yellow
      {% elif n == 3 %} orange
      {% elif n >= 4 %} red {% endif %}
```

### Comparativa de totes les estacions (Statistics Graph)

```yaml
type: statistics-graph
title: Temperatures — Totes les estacions
entities:
  - sensor.encamp_encamp_temperature
  - sensor.els_plans_de_canillo_canillo_temperature
  - sensor.la_cortinada_ordino_temperature
  - sensor.certes_sant_julia_de_loria_temperature
  - sensor.escaldes_engordany_centre_escaldes_engordany_temperature
  - sensor.escaldes_engordany_sa_calma_escaldes_engordany_temperature
stat_types:
  - mean
  - min
  - max
days_to_show: 7
```

---

## 🤖 Automatitzacions d'exemple

### Avís per Telegram quan el perill d'allaus és alt

```yaml
automation:
  - alias: "🏔️ Avís perill d'allaus Andorra"
    description: "Notificació quan qualsevol zona arriba a perill marcat o superior"
    trigger:
      - platform: state
        entity_id: binary_sensor.avis_allaus_actiu
        to: "on"
    condition:
      - condition: template
        value_template: >
          {{ now().hour >= 7 and now().hour <= 22 }}
    action:
      - service: notify.telegram_jan
        data:
          message: >
            ⛷️ *AVÍS D'ALLAUS ACTIU al Principat d'Andorra*

            🔴 Nord: {{ states('sensor.nivell_de_perill_allaus_nord') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_nord', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_nord') }}

            🔴 Centre: {{ states('sensor.nivell_de_perill_allaus_centre') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_centre', 'level_name') }}
            — {{ states('sensor.tipus_de_neu_zona_centre') }}

            🔴 Sud: {{ states('sensor.nivell_de_perill_allaus_sud') }}/5
            — {{ state_attr('sensor.nivell_de_perill_allaus_sud', 'level_name') }}

            📅 Vàlid fins: {{ states('sensor.butlleti_valid_fins') }}
            🔗 [Butlletí complet](https://www.meteo.ad/neu)
```

### Avís quan l'estació porta més d'1 hora sense actualitzar

```yaml
automation:
  - alias: "📡 Estació Encamp offline"
    trigger:
      - platform: template
        value_template: >
          {% set last = states('sensor.encamp_encamp_ultima_actualitzacio') %}
          {% if last not in ['unknown','unavailable'] %}
            {% set dt = strptime(last, '%d/%m/%Y %H:%M UTC') %}
            {{ (now().utctimetuple() | list | sum) - (dt.utctimetuple() | list | sum) > 3600 }}
          {% else %}
            false
          {% endif %}
        for: "00:05:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            📡 L'estació d'Encamp no ha actualitzat dades en més d'1 hora.
            Última actualització: {{ states('sensor.encamp_encamp_ultima_actualitzacio') }}
```

### Avís de gelada matinal

```yaml
automation:
  - alias: "🌡️ Avís de gelada — Encamp"
    trigger:
      - platform: numeric_state
        entity_id: sensor.encamp_encamp_temperature
        below: 0
    condition:
      - condition: time
        after: "06:00:00"
        before: "10:00:00"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            🌡️ Temperatura sota zero a Encamp!
            Temperatura actual: {{ states('sensor.encamp_encamp_temperature') }}°C
            Mínima del dia: {{ states('sensor.encamp_encamp_daily_min_temperature') }}°C
```

### Notificació de nova estació detectada

> Aquesta automatització és automàtica — la integració ja crea una notificació persistent a HA
> si detecta un codi d'estació nou al Principat. No cal configurar res addicional.

---

## 🔄 Afegir una nova estació (quan aparegui una nova al Principat)

Si reps una notificació de nova estació detectada, el procés és molt senzill:

1. Comprova el codi nou a `https://www.meteoclimatic.net/mapinfo/ADAND`
2. Edita **només** `custom_components/meteo_andorra/const.py` afegint l'estació al bloc `PARISHES`
3. Reinicia Home Assistant
4. Afegeix la nova instància des de la integració

---

## 📝 Notes tècniques

- **Polling:** Estacions cada 30 min · Butlletí d'allaus cada 60 min · Detecció d'estacions noves cada 24h
- **Caché:** Si una estació queda offline, les entitats mantenen l'últim valor conegut fins a recuperar connexió
- **Valor -99:** Meteoclimatic usa -99 com a indicador de sensor avariat — la integració el filtra i mostra `None`
- **Domicili tècnic:** `meteo_andorra` (no canviar per compatibilitat amb instal·lacions existents)

---

## Llicència

MIT © [@janfajessen](https://github.com/janfajessen)
