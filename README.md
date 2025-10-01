Qué es: mini app Streamlit para explorar Airbnb NYC.

Cómo correr local:
    conda create -n airbnb python=3.12 -y
    conda activate airbnb
    pip install -r requirements.txt
    python -m streamlit run app.py


Dataset: colocar data/airbnb_nyc.csv con columnas mencionadas.

Funciones: distribución de precios por borough/barrio, scatter reviews–ocupación, mapa de calor.

Deploy: igual que en tu proyecto McDonald’s (Streamlit Cloud / Render).

Render Start command:

streamlit run app.py --server.port $PORT --server.address 0.0.0.0