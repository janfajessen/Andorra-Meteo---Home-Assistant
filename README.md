<div align="center">

# Andorra Meteo

<img src="brands/icon@2x.png" width="250"/>

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

| Nivell | Nom | Color |
|---|---|---|
| 0 | Sense perill | ⬜ |
| 1 | Feble | 🟩 |
| 2 | Limitat | 🟨 |
| 3 | Marcat | 🟧 |
| 4 | Fort | 🟥 |
| 5 | Molt fort | 🟫 |

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

<details>
<summary>🇪🇸 Español</summary>

## Andorra Meteo — Integración para Home Assistant

Integración de Home Assistant para datos meteorológicos y peligro de aludes en el Principado de Andorra. Utiliza la red de estaciones de [Meteoclimatic](https://www.meteoclimatic.net/) y el boletín de aludes del [Servei Meteorològic Nacional](https://www.meteo.ad/).

### Instalación

**Via HACS:** Añade `https://github.com/janfajessen/andorra_meteo` como repositorio personalizado de tipo Integration, busca "Andorra Meteo" e instala. Reinicia Home Assistant.

**Manual:** Copia la carpeta `custom_components/meteo_andorra/` a `config/custom_components/` y reinicia.

### Configuración

En **Configuración → Dispositivos y servicios → + Añadir integración**, busca **Andorra Meteo**. Un único desplegable muestra todas las parroquias y el boletín de aludes. Escaldes-Engordany tiene dos estaciones (Centre y Sa Calma). El boletín de aludes solo se puede añadir una vez.

### Estaciones disponibles

Els Plans de Canillo (1.780 m) · Encamp (1.270 m) · La Cortinada, Ordino (1.330 m) · Certés, Sant Julià de Lòria (1.350 m) · Escaldes-Engordany Centre (1.050 m) · Escaldes-Engordany Sa Calma (1.180 m)

### Entidades

Cada estación crea un dispositivo con 14 sensores meteorológicos (temperatura, humedad, presión, viento, precipitación, dirección del viento, última actualización) y una entidad `weather` con icono de condición real.

El boletín de aludes crea un dispositivo con sensores de nivel de peligro por zona (Norte/Centro/Sur, escala 0–5), sensores de tipo de nieve por zona y un `binary_sensor` que se activa cuando cualquier zona alcanza nivel ≥ 3 (Marcado).

Si la estación queda offline, los sensores conservan el último valor conocido en lugar de mostrar "no disponible".

</details>

<details>
<summary>🇫🇷 Français</summary>

## Andorra Meteo — Intégration Home Assistant

Intégration Home Assistant pour les données météorologiques et le danger d'avalanche en Principauté d'Andorre. Utilise le réseau de stations [Meteoclimatic](https://www.meteoclimatic.net/) et le bulletin d'avalanche du [Servei Meteorològic Nacional](https://www.meteo.ad/).

### Installation

**Via HACS:** Ajoutez `https://github.com/janfajessen/andorra_meteo` comme dépôt personnalisé de type Integration, cherchez "Andorra Meteo" et installez. Redémarrez Home Assistant.

**Manuel:** Copiez le dossier `custom_components/meteo_andorra/` dans `config/custom_components/` et redémarrez.

### Configuration

Dans **Paramètres → Appareils et services → + Ajouter une intégration**, cherchez **Andorra Meteo**. Un seul menu déroulant affiche toutes les paroisses et le bulletin d'avalanche. Escaldes-Engordany dispose de deux stations (Centre et Sa Calma). Le bulletin d'avalanche ne peut être ajouté qu'une seule fois.

### Stations disponibles

Els Plans de Canillo (1.780 m) · Encamp (1.270 m) · La Cortinada, Ordino (1.330 m) · Certés, Sant Julià de Lòria (1.350 m) · Escaldes-Engordany Centre (1.050 m) · Escaldes-Engordany Sa Calma (1.180 m)

### Entités

Chaque station crée un appareil avec 14 capteurs météo (température, humidité, pression, vent, précipitations, direction du vent, dernière mise à jour) et une entité `weather` avec icône de condition réelle.

Le bulletin d'avalanche crée un appareil avec des capteurs de niveau de danger par zone (Nord/Centre/Sud, échelle 0–5), des capteurs de type de neige par zone et un `binary_sensor` qui s'active quand une zone atteint le niveau ≥ 3 (Marqué).

En cas de panne de station, les capteurs conservent la dernière valeur connue plutôt que d'afficher "indisponible".

</details>

<details>
<summary>🇬🇧 English</summary>

## Andorra Meteo — Home Assistant Integration

Home Assistant integration for real-time weather data and avalanche danger in the Principality of Andorra. Uses the [Meteoclimatic](https://www.meteoclimatic.net/) station network and the official avalanche bulletin from the [Servei Meteorològic Nacional](https://www.meteo.ad/).

### Installation

**Via HACS:** Add `https://github.com/janfajessen/andorra_meteo` as a custom repository of type Integration, search for "Andorra Meteo" and install. Restart Home Assistant.

**Manual:** Copy the `custom_components/meteo_andorra/` folder to `config/custom_components/` and restart.

### Configuration

Go to **Settings → Devices & services → + Add integration** and search for **Andorra Meteo**. A single dropdown shows all parishes and the avalanche bulletin. Escaldes-Engordany has two stations (Centre and Sa Calma). The avalanche bulletin can only be added once.

### Available stations

Els Plans de Canillo (1,780 m) · Encamp (1,270 m) · La Cortinada, Ordino (1,330 m) · Certés, Sant Julià de Lòria (1,350 m) · Escaldes-Engordany Centre (1,050 m) · Escaldes-Engordany Sa Calma (1,180 m)

### Entities

Each station creates a device with 14 weather sensors (temperature, humidity, pressure, wind, precipitation, wind direction, last update) and a `weather` entity with a real condition icon.

The avalanche bulletin creates a device with danger level sensors per zone (North/Centre/South, scale 0–5), snow type sensors per zone and a `binary_sensor` that activates when any zone reaches level ≥ 3 (Considerable).

If a station goes offline, sensors retain the last known value instead of showing "unavailable".

</details>

<details>
<summary>🇵🇹 Português</summary>

## Andorra Meteo — Integração para Home Assistant

Integração de Home Assistant para dados meteorológicos e perigo de avalanche no Principado de Andorra. Utiliza a rede de estações [Meteoclimatic](https://www.meteoclimatic.net/) e o boletim de avalanches do [Servei Meteorològic Nacional](https://www.meteo.ad/).

### Instalação

**Via HACS:** Adicione `https://github.com/janfajessen/andorra_meteo` como repositório personalizado do tipo Integration, procure "Andorra Meteo" e instale. Reinicie o Home Assistant.

**Manual:** Copie a pasta `custom_components/meteo_andorra/` para `config/custom_components/` e reinicie.

### Configuração

Vá a **Configurações → Dispositivos e serviços → + Adicionar integração** e procure **Andorra Meteo**. Um único menu suspenso mostra todas as paróquias e o boletim de avalanches. Escaldes-Engordany tem duas estações (Centre e Sa Calma). O boletim de avalanches só pode ser adicionado uma vez.

### Estações disponíveis

Els Plans de Canillo (1.780 m) · Encamp (1.270 m) · La Cortinada, Ordino (1.330 m) · Certés, Sant Julià de Lòria (1.350 m) · Escaldes-Engordany Centre (1.050 m) · Escaldes-Engordany Sa Calma (1.180 m)

### Entidades

Cada estação cria um dispositivo com 14 sensores meteorológicos (temperatura, humidade, pressão, vento, precipitação, direção do vento, última atualização) e uma entidade `weather` com ícone de condição real.

O boletim de avalanches cria um dispositivo com sensores de nível de perigo por zona (Norte/Centro/Sul, escala 0–5), sensores de tipo de neve por zona e um `binary_sensor` que ativa quando qualquer zona atinge nível ≥ 3 (Considerável).

Se uma estação ficar offline, os sensores mantêm o último valor conhecido em vez de mostrar "indisponível".

</details>

---

<div align="center">

Fet amb ❤️ per [@janfajessen](https://github.com/janfajessen) · MIT License

*Si trobes una nova estació al Principat, obre una issue o un PR!*

</div>



## Llicència

MIT © [@janfajessen](https://github.com/janfajessen)
