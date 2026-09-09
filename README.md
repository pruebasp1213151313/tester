# Load Tester (Locust)

Pruebas de carga y rendimiento para tu propio sitio web. Mide cuánta
carga aguanta tu sitio antes de degradarse, con un dashboard en vivo
que muestra peticiones por segundo, tiempos de respuesta (media,
mediana, percentil 95) y tasa de errores.

> **Uso responsable.** Ejecuta esto únicamente contra sitios que son
> tuyos o para los que tienes autorización explícita por escrito. Lanzar
> carga contra infraestructura ajena sin permiso es ilegal en la mayoría
> de las jurisdicciones. Empieza siempre con pocos usuarios y sube poco
> a poco.

## Requisitos

- Python 3.9 o superior

## Instalación

```bash
git clone https://github.com/tuusuario/load-tester.git
cd load-tester

python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Uso

### Dashboard web (recomendado)

```bash
locust -f locustfile.py --host https://tu-sitio.com
```

Abre http://localhost:8089. Ahí eliges el número de usuarios y la tasa
de arranque, pulsas *Start* y ves las gráficas en tiempo real.

### Modo headless (para CI o corridas automáticas)

```bash
locust -f locustfile.py --host https://tu-sitio.com \
    --headless -u 100 -r 10 -t 2m --html reporte.html
```

- `-u 100` — 100 usuarios virtuales concurrentes
- `-r 10` — arranca 10 usuarios por segundo
- `-t 2m` — corre durante 2 minutos
- `--html reporte.html` — guarda un reporte al terminar

### Escenario con login

```bash
locust -f scenarios/con_login.py --host https://tu-sitio.com
```

## Cómo encontrar el punto de quiebre

La idea del "cuánto aguanta" es subir la carga de forma escalonada y
observar cuándo empieza a degradarse:

1. Corre con pocos usuarios (ej. `-u 10`) y anota la latencia base.
2. Sube gradualmente (`-u 50`, `-u 100`, `-u 200`...).
3. El punto de quiebre es donde el percentil 95 de la latencia se
   dispara o la tasa de errores empieza a subir. Esa es la capacidad
   real de tu sitio.

## Estructura

```
load-tester/
├── README.md
├── requirements.txt
├── .gitignore
├── locustfile.py            # escenario principal (navegación)
├── scenarios/
│   └── con_login.py         # escenario con autenticación
└── .github/
    └── workflows/
        └── loadtest.yml     # corrida manual desde GitHub Actions
```

## Personalización

En `locustfile.py`:

- Ajusta las rutas (`/`, `/productos`, `/buscar`) a las de tu sitio.
- El decorador `@task(n)` fija el peso: un peso mayor significa que esa
  página se visita más a menudo.
- `wait_time = between(1, 5)` es el tiempo de "pensar" entre acciones.
  Súbelo para simular usuarios más lentos, bájalo para carga más
  agresiva (pero realista).
