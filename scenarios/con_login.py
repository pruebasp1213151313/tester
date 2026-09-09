"""
Escenario con flujo de login + validación de respuestas.

Muestra cómo:
  - autenticarse una vez por usuario virtual
  - encadenar pasos (login -> ver dashboard -> hacer una acción)
  - validar que la respuesta es la esperada y marcar fallos manualmente

Uso:
    locust -f scenarios/con_login.py --host https://tu-sitio.com
"""

from locust import HttpUser, task, between


class UsuarioAutenticado(HttpUser):
    wait_time = between(2, 6)

    def on_start(self):
        # Ajusta los campos y la ruta a tu formulario real de login.
        with self.client.post(
            "/login",
            data={"username": "usuario_de_prueba", "password": "clave_de_prueba"},
            catch_response=True,
            name="login",
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Login falló: HTTP {resp.status_code}")

    @task
    def ver_dashboard(self):
        with self.client.get(
            "/dashboard", catch_response=True, name="dashboard"
        ) as resp:
            # Marca como fallo si el contenido no es el esperado,
            # aunque el status sea 200.
            if "Bienvenido" not in resp.text:
                resp.failure("No se encontró el contenido esperado en /dashboard")

    @task
    def ver_perfil(self):
        self.client.get("/perfil", name="perfil")
