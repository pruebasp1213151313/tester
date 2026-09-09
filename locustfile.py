"""
Load test principal - AC Group.

Simula usuarios navegando el sitio de forma realista para medir
rendimiento (latencia, throughput, tasa de errores) bajo carga, y
encontrar el punto donde el sitio empieza a degradarse.

Uso RECOMENDADO (empezar bajo e ir subiendo):
    # UI web con dashboard en vivo
    locust -f locustfile.py --host https://staging.acgroup.com.py
    # abre http://localhost:8089 y empieza con 20 usuarios, luego 50, 100...

    # Modo headless escalonado (ejemplo: 50 usuarios, arranque 5/s, 3 min)
    locust -f locustfile.py --host https://staging.acgroup.com.py \
        --headless -u 50 -r 5 -t 3m --html reporte.html

NO empieces con cientos o miles de usuarios: eso solo confirma que se
cae (cosa que ya sabes). Sube escalonadamente para hallar el umbral real.

IMPORTANTE: usalo solo contra sitios propios o con autorizacion escrita.
"""

from locust import HttpUser, task, between


class UsuarioWeb(HttpUser):
    # Tiempo de "pensar" entre acciones: entre 1 y 5 segundos.
    # Imita a un usuario real, no un flood.
    wait_time = between(1, 5)

    def on_start(self):
        """Se ejecuta una vez cuando cada usuario virtual arranca."""
        # Si el sitio necesita login, iria aqui. Ajusta a tu formulario real:
        #
        # self.client.post("/login", data={
        #     "username": "usuario_de_prueba",
        #     "password": "clave_de_prueba",
        # })
        pass

    @task(3)
    def home(self):
        """Pagina principal. Peso 3 = se visita 3x mas que las demas."""
        self.client.get("/", name="home")

    @task(2)
    def paginas_internas(self):
        """Paginas internas del sitio principal."""
        self.client.get("/contacto", name="contacto")
        self.client.get("/empresa", name="empresa")

    @task(1)
    def busqueda(self):
        """Busqueda con parametro."""
        self.client.get("/buscar", params={"q": "ejemplo"}, name="busqueda")