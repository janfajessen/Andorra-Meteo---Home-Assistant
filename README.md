<div align="center">

# Andorra Meteo

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

Integració de Home Assistant per al temps i el perill d'allaus del Principat d'Andorra, amb dades de la xarxa [Meteoclimatic](https://www.meteoclimatic.net/) i el [Servei Meteorològic Nacional](https://www.meteo.ad/).

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

---

## Fonts de dades

| Mòdul | Font | Freqüència |
|---|---|---|
| Estació meteorològica | Meteoclimatic — feed RSS públic | 30 min |
| Butlletí d'allaus | meteo.ad — Servei Meteorològic Nacional | 60 min |

---

## Instal·lació

### Via HACS (recomanat)

1. Obre **HACS → Integracions → ⋮ → Repositoris personalitzats**.
2. Afegeix `https://github.com/janfajessen/meteo_andorra` com a tipus **Integration**.
3. Cerca **Meteo Andorra** i instal·la.
4. Reinicia Home Assistant.
<img src="brands/icon@2x.png" width="100"/>

### Manual

1. Copia la carpeta `custom_components/meteo_andorra` al directori `config/custom_components/`.
2. Reinicia Home Assistant.

---

## Configuració

A **Configuració → Dispositius i serveis → + Afegeix integració**, cerca **Meteo Andorra**.

El primer pas mostra un desplegable únic:

```
Canillo
Encamp
Ordino
Sant Julià de Lòria
Escaldes-Engordany
Butlletí d'allaus — Principat d'Andorra
```

- Si tries una **parròquia amb una sola estació** → es configura directament.
- Si tries **Escaldes-Engordany** → apareix un segon pas per escollir entre les dues estacions disponibles.
- Si tries **Butlletí d'allaus** → es configura sol, sense cap pas addicional.

> Pots afegir **múltiples estàcions** tornant a afegir la integració. El butlletí d'allaus només es pot afegir **una vegada**.

### Estacions disponibles

| Parròquia | Estació |
|---|---|
| Canillo | ```El Pas de Canillo``` |
| Encamp | ```Encamp``` |
| Ordino | ```Cortinada``` |
| Sant Julià de Lòria | ```Certés``` |
| Escaldes-Engordany | ```Centre``` |
| Escaldes-Engordany | ```Sa Calma``` |

---

## Entitats creades

### Estació meteorològica

Cada estació crea un **dispositiu** amb:

| Entitat | Tipus | Unitat |
|---|---|---|
| ```Temperatura``` | sensor | °C |
| ```Temperatura màxima diària``` | sensor | °C |
| ```Temperatura mínima diària``` | sensor | °C |
| ```Humitat``` | sensor | % |
| ```Humitat màxima diària``` | sensor | % |
| ```Humitat mínima diària``` | sensor | % |
| ```Pressió``` | sensor | hPa |
| ```Pressió màxima diària``` | sensor | hPa |
| ```Pressió mínima diària``` | sensor | hPa |
| ```Velocitat del vent``` | sensor | km/h |
| ```Ratxa màxima diària``` | sensor | km/h |
| ```Direcció del vent``` | sensor | ° |
| ```Precipitació diària``` | sensor | mm |
| ```weather``` |**Temps** |  — amb icona de condició |

La condició meteorològica (sol, núvols, pluja, neu, etc.) prové directament del feed i es mostra com a icona a la targeta `weather`.

### Butlletí d'allaus

Un sol dispositiu **Butlletí d'allaus — Principat d'Andorra** amb:

| Entitat | Tipus | Descripció |
|---|---|---|
| Perill d'allaus — Zona nord | sensor | Nivell 1–5 (escala europea) |
| Perill d'allaus — Zona centre | sensor | Nivell 1–5 |
| Perill d'allaus — Zona sud | sensor | Nivell 1–5 |
| Butlletí vàlid fins | sensor | Data de caducitat |
| Avís d'allaus actiu | binary_sensor | `on` si qualsevol zona ≥ 3 (Marcat) |

Els sensors de perill inclouen atributs amb el tipus de problema, la tendència i els textos descriptius del butlletí.

**Escala europea de perill d'allaus:**

| Nivell | Nom |
|---|---|
| 1 | Feble |
| 2 | Limitat |
| 3 | Marcat |
| 4 | Fort |
| 5 | Molt fort |

---

## Exemple d'automatització

```yaml
automation:
  - alias: "Avís perill d'allaus"
    trigger:
      - platform: state
        entity_id: binary_sensor.avis_allaus_actiu
        to: "on"
    action:
      - service: notify.telegram_jan
        data:
          message: >
            ⛷️ Perill d'allaus ACTIU al Principat!
            Nord: {{ states('sensor.perill_allaus_zona_nord') }}
            Centre: {{ states('sensor.perill_allaus_zona_centre') }}
            Sud: {{ states('sensor.perill_allaus_zona_sud') }}
```

---

<details>
<summary>🇪🇸 Español</summary>

Integración de Home Assistant para el tiempo y el peligro de aludes del Principado de Andorra. Utiliza la red de estaciones de [Meteoclimatic](https://www.meteoclimatic.net/) y el boletín de aludes del [Servei Meteorològic Nacional](https://www.meteo.ad/).

**Instalación:** Via HACS añadiendo `https://github.com/janfajessen/meteo_andorra` como repositorio personalizado, o copiando `custom_components/meteo_andorra/` manualmente y reiniciando Home Assistant.

**Configuración:** Al añadir la integración aparece un único desplegable con las parroquias y la opción de boletín de aludes. Escaldes-Engordany tiene dos estaciones (Centre y Sa Calma) y pide una segunda elección. El boletín de aludes solo se puede añadir una vez.

**Entidades:** Cada estación crea un dispositivo con 13 sensores meteorológicos y una entidad `weather` con icono de condición. El boletín de aludes crea un dispositivo con sensores de nivel de peligro por zona (Norte/Centro/Sur, escala 1–5) y un `binary_sensor` que se activa cuando cualquier zona alcanza nivel ≥ 3.

</details>

<details>
<summary>🇬🇧 English</summary>

Home Assistant integration for weather data and avalanche danger in the Principality of Andorra. Uses the [Meteoclimatic](https://www.meteoclimatic.net/) station network and the avalanche bulletin from the [Servei Meteorològic Nacional](https://www.meteo.ad/).

**Installation:** Via HACS by adding `https://github.com/janfajessen/meteo_andorra` as a custom repository, or by copying `custom_components/meteo_andorra/` manually and restarting Home Assistant.

**Configuration:** A single dropdown shows all parishes plus the avalanche bulletin option. Escaldes-Engordany has two stations (Centre and Sa Calma) and prompts a second selection. The avalanche bulletin can only be added once.

**Entities:** Each station creates a device with 13 weather sensors and a `weather` entity with condition icon. The avalanche bulletin creates a device with danger level sensors per zone (North/Centre/South, scale 1–5) and a `binary_sensor` that activates when any zone reaches level ≥ 3.

</details>

<details>
<summary>🇫🇷 Français</summary>

Intégration Home Assistant pour la météo et le danger d'avalanche en Principauté d'Andorre. Utilise le réseau de stations [Meteoclimatic](https://www.meteoclimatic.net/) et le bulletin d'avalanche du [Servei Meteorològic Nacional](https://www.meteo.ad/).

**Installation:** Via HACS en ajoutant `https://github.com/janfajessen/meteo_andorra` comme dépôt personnalisé, ou en copiant `custom_components/meteo_andorra/` manuellement et en redémarrant Home Assistant.

**Configuration:** Un seul menu déroulant affiche toutes les paroisses et l'option bulletin d'avalanche. Escaldes-Engordany dispose de deux stations (Centre et Sa Calma) et demande un second choix. Le bulletin d'avalanche ne peut être ajouté qu'une seule fois.

**Entités:** Chaque station crée un appareil avec 13 capteurs météo et une entité `weather` avec icône de condition. Le bulletin d'avalanche crée un appareil avec des capteurs de niveau de danger par zone (Nord/Centre/Sud, échelle 1–5) et un `binary_sensor` qui s'active quand une zone atteint le niveau ≥ 3.

</details>

<details>
<summary>🇵🇹 Português</summary>

Integração Home Assistant para dados meteorológicos e perigo de avalanche no Principado de Andorra. Utiliza a rede de estações [Meteoclimatic](https://www.meteoclimatic.net/) e o boletim de avalanches do [Servei Meteorològic Nacional](https://www.meteo.ad/).

**Instalação:** Via HACS adicionando `https://github.com/janfajessen/meteo_andorra` como repositório personalizado, ou copiando `custom_components/meteo_andorra/` manualmente e reiniciando o Home Assistant.

**Configuração:** Um único menu suspenso mostra todas as paróquias e a opção de boletim de avalanches. Escaldes-Engordany tem duas estações (Centre e Sa Calma) e solicita uma segunda seleção. O boletim de avalanches só pode ser adicionado uma vez.

**Entidades:** Cada estação cria um dispositivo com 13 sensores meteorológicos e uma entidade `weather` com ícone de condição. O boletim de avalanches cria um dispositivo com sensores de nível de perigo por zona (Norte/Centro/Sul, escala 1–5) e um `binary_sensor` que ativa quando qualquer zona atinge nível ≥ 3.

</details>

---

## Llicència

MIT © [@janfajessen](https://github.com/janfajessen)
