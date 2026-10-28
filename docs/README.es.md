<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · **Español** · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Un sistema operativo para un equipo de agentes de IA.** Un solo comando convierte una carpeta común en una oficina disciplinada: un tablero único del que trabajan todos los agentes, en cualquier plataforma; una puerta de calidad independiente; gobernanza de decisiones; un registro de auditoría completo; métricas de rendimiento que se exportan a Power BI; y un sitio de gestión que funciona desde un único archivo HTML.

Python 3.9 o posterior, sin dependencias, sin servidor. Código abierto, con licencia MIT.

Sitio web: https://hakamidev.github.io/ProjectForge/

## Instalación

Una sola línea, pegada en una terminal. Descarga la herramienta, la ejecuta, hace cuatro preguntas y después abre su sitio de gestión.

macOS y Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

El sitio también permite elegir primero la plataforma y el idioma preferido; ambos se incorporan al comando de instalación y quedan preseleccionados en el asistente.

## Qué resuelve

- **Los chats olvidan.** Las reglas y las fichas de rol viven en la carpeta, no en la memoria del chat, de modo que cualquier chat puede retomar el trabajo.
- **Los agentes chocan.** Un tablero numerado único; «en curso» bloquea una fila; una protección por suma de verificación evita escrituras en conflicto.
- **Resultados sin revisar.** Un responsable de aseguramiento de la calidad dictamina si se aprueba o se rechaza antes de que algo llegue al propietario.
- **Decisiones estancadas.** Como máximo cinco decisiones abiertas y una regla de 48 horas, transcurridas las cuales prevalece la recomendación.
- **Nada se mide.** `report` ofrece la tasa de entrega, el tiempo de ciclo, la tasa de aprobación de QA y la carga por rol; `export` escribe archivos CSV para Power BI.
- **Sin rendición de cuentas.** Cada escritura en el tablero queda registrada: quién, cuándo y qué.
- **Datos sensibles en herramientas externas.** Una política de datos vinculante, con clasificación y herramientas aprobadas.

## Qué incluye

- **80 especializaciones** (estrategia, restauración, bienes raíces, software, RR. HH., educación y más) con más de 330 roles listos que se añaden con un clic.
- **130 habilidades listas en 18 grupos.** Una habilidad es un archivo breve que describe cuándo usarla, sus pasos, su resultado y su criterio de aceptación, de modo que un empleado la aplica en lugar de improvisar.
- **Cuatro plataformas:** Claude, ChatGPT, Grok y Gemini. Cada empleado puede trabajar en una plataforma distinta.
- **27 idiomas de interfaz** en el sitio web y en el asistente. El idioma preferido es el de la gestión de todo el sistema y el que se usa con los empleados.
- **Un sitio de gestión** desde un solo archivo HTML: tablero, equipo, decisiones, métricas, una biblioteca de comandos listos y un motor de atención que señala lo que está atrasado o a la espera de usted.

## Comandos

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Plataformas

| Plataforma | Cómo se configura el equipo |
| --- | --- |
| Claude | Cree un proyecto con el nombre de su proyecto y añada la carpeta generada. |
| ChatGPT | Cree un proyecto y suba los archivos de la carpeta. |
| Grok | Cree un proyecto, pegue el comando de Compass en sus instrucciones y añada los archivos. |
| Gemini | Cree un Gem por empleado, pegue su comando en las instrucciones y añada los archivos en Knowledge. |

Suba los archivos desde la carpeta del proyecto en su ubicación original y vuelva a subir lo que cambie. Hasta donde sabemos, Grok y Gemini no escriben directamente en la carpeta, así que traslade usted mismo sus resultados a la carpeta. Los pasos siguen la documentación pública en el momento de la redacción; las interfaces y los límites los fijan esas plataformas y pueden cambiar.

## Limitaciones actuales

- El asistente y el sitio web aparecen en 27 idiomas, pero los archivos generados del proyecto (reglas, fichas de rol, tablero) y el sitio de gestión están escritos por ahora en árabe. A los empleados se les indica en qué idioma trabajar y le responden en él.
- Los nombres de archivo, los comandos y los términos de estado del tablero se mantienen en árabe, porque la herramienta los lee literalmente.
- La instalación en Windows aún no se ha probado en una máquina real.

## Para desarrolladores

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

El código fuente está en `forge/`; `tools/build-single.py` genera la herramienta de un solo archivo en `dist/`. Las plantillas están en `forge/templates/` y el sitio público en `site/`.

## Licencia

MIT.
