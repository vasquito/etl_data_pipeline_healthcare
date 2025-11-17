import panel as pn

pn.extension()


def view():
    content = pn.Column(
        pn.pane.Markdown(
            "Este dashboard ejecuta un pipeline ETL completo sobre datos abiertos de centros médicos "
            "de la Ciudad Autónoma de Buenos Aires (CABA), integrando geolocalización, almacenamiento local "
            "y visualización interactiva. "
            "El pipeline ya está operativo y modularizado. Los datos se descargan, transforman y almacenan "
            "de forma reproducible. Las vistas de **Datos** y **Mapa** permiten explorar los resultados "
            "de forma interactiva.\n\n"
            "🔄 **Etapas del Pipeline**: Ingesta full de conjuntos de datos sobre los centros medicos de Buenos Aires\n\n"
            "- **Descarga automática** de un archivo GeoJSON desde el portal de datos abiertos de CABA\n"
            "- **Almacenamiento local** del archivo en un bucket S3 simulado (local)\n"
            "- **Transformación y mapeo** de los datos geográficos y atributos médicos\n"
            "- **Persistencia** en una base de datos SQLite, incluyendo coordenadas y metadatos\n"
            "- **Visualización** en dos páginas del dashboard:\n"
            "  - 📊 **Datos**: tabla interactiva y gráficos\n"
            "  - 🌍 **Mapa**: puntos geolocalizados sobre Leaflet\n\n"
            "🧱 **Tecnologías utilizadas**\n\n"
            "- Python 3.13\n"
            "- Dataset BA\n"
            "- S3 (Localstack como AWS Local)\n"
            "- SQLite (Persistencia como BigQuery)\n"
            "- Libraries Python\n"
            "  - Panel (Visualizacion)\n"
            "  - Panda\n"
            "  - Folium - Leaflet (SIG - GeoLocation)\n"
            "  - Graphviz (Flujos)\n"
            "  - matplotlib y seaborn\n\n"
            "🧪 Test: Docker Local"
        )
    )

    return pn.Column(content, height=450, scroll=True)
