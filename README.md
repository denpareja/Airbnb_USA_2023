🏡 Airbnb Explorer (USA 2023)

Mini app en Streamlit para explorar listados de Airbnb por ciudad, con filtros interactivos, gráficos (Plotly) y un mapa. Permite entender la distribución de precios por barrio, la relación entre reviews y ocupación y visualizar hotspots.


🚀 Demo & enlaces

🟢 Live (Render): https://airbnb-usa-2023.onrender.com/

🧑‍💻 Repositorio (GitHub): https://github.com/denpareja/Airbnb_USA_2023

🗂️ Dataset en el repo: airbnb_data_2023.csv

🔴 Streamlit Cloud (opcional): si también lo despliegas allí, agrega tu enlace aquí
https://<tu-app>.streamlit.app/

✨ Funcionalidades

Filtros: ciudad, rango de precio por noche, tipo de habitación (private, entire home/apt, shared, hotel) y barrio (Top 50 por cantidad).

KPIs: # de listados, precio mediano, reviews/mes (prom.), ocupación aprox. (estimada a partir de reviews).

Gráficos (Plotly)

Distribución de precios por barrio (boxplot, Top 15 por cantidad).

Relación reviews vs ocupación (dispersión).

Mapa: densidad de listados / puntos por barrio (Plotly).

Tabla: vista previa/descarga de los datos filtrados.

📁 Estructura del proyecto
Airbnb_USA_2023/
├─ app.py                 # App principal (Streamlit)
├─ airbnb_data_2023.csv   # Dataset (incluido en el repo)
├─ requirements.txt       # Dependencias para reproducir/desplegar
├─ README.md              # Este archivo
└─ LICENSE

🧪 Dataset

El archivo esperado es airbnb_data_2023.csv (incluido). Columnas típicas (ajusta si tu CSV difiere):

Columna	Ejemplo	Notas
city	Chicago	Ciudad del listado
neighbourhood	Loop	Barrio / zona
room_type	Entire home/apt	Tipo de habitación
price	145	Precio por noche (USD)
reviews_per_month	2.1	Reviews/mes
number_of_reviews	57	Total de reviews
availability_365	120	Días disponibles al año
latitude,longitude	41.88,-87.63	Coordenadas (para mapa)
▶️ Cómo correr localmente

Con conda (recomendado):

conda create -n airbnb python=3.12 -y
conda activate airbnb
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py


Abre el navegador en http://localhost:8501.

📦 Requisitos

requirements.txt (ejemplo compatible con Render/Linux+py312):

streamlit==1.37.1
pandas==2.2.3
plotly==5.24.1


Nota: fijar pandas==2.2.3 evita conflictos de wheels en Render.
Si subes de versión, prueba primero localmente.

☁️ Deploy
Opción A) Render (gratis)

Conecta tu GitHub en Render y selecciona el repo denpareja/Airbnb_USA_2023.

Runtime: Python.

Build Command (opcional, Render autodetecta)

pip install -r requirements.txt


Start Command

streamlit run app.py --server.port $PORT --server.address 0.0.0.0


Deploy y listo. URL pública (ej.): https://airbnb-usa-2023.onrender.com/.

Si ves 502 Bad Gateway, revisa los Logs y confirma que se detecta el puerto $PORT y que el start command es el de arriba.

Opción B) Streamlit Cloud (opcional)

En https://share.streamlit.io/
 selecciona tu repo y rama main.

Main file path: app.py.

Deploy y copia la URL https://<tu-app>.streamlit.app/.

Vuelve a este README y reemplaza el enlace de Streamlit en la sección Demo & enlaces.

🧰 Stack

Streamlit para la UI.

Pandas para carga/filtrado del dataset.

Plotly para gráficos interactivos.

(Opcional) Folium si quisieras mapas de calor estilo leaflet.

📝 Roadmap / ideas

 Filtro por fechas/temporadas.

 Métricas por host (superhost vs. no).

 Mejorar el modelo de ocupación estimada.

 Exportar tabla filtrada a CSV/Excel desde la app.

🔗 Proyecto relacionado

🍔 McDonald’s Nutrition App

Live (Render): https://mcdonalds-nutrition-app.onrender.com/

Repo: https://github.com/denpareja/mcdonalds-nutrition-app

📜 Licencia

Este proyecto está bajo la licencia MIT. Ver LICENSE
.