import folium
import panel as pn

class MedicalCentersMap:
    def __init__(self, df):
        self.df = df

    def view(self):
        pn.extension()

        if self.df.empty:
            selector_comuna = pn.widgets.Select(name="Filtrar por comuna", options=["Todos"], value="Todos",width=250)
            mapa_html = pn.pane.HTML("", min_height=500, sizing_mode="stretch_width")
            def generar_mapa(comuna):
                centro = [-34.6037, -58.3816] # Obelisco, centro de CABA
                mapa = folium.Map(
                    location=centro,
                    zoom_start=12,
                    control_scale=False,
                    zoom_control=False,  # oculta el control de zoom
                    scrollWheelZoom=False,  # desactiva zoom con scroll
                    dragging=False  # impide mover el mapa
                )

                # Renderizar mapa como HTML en Panel
                html = mapa._repr_html_().replace('height:100%;', 'height:500px;')
                mapa_html.object = html
        else:
            df_renamed = self.df.rename(columns={
                "nombre": "Codigo",
                "barrio": "Barrio",
                "esp": "Especialidad",
                "comuna": "Comuna",
                "telefono": "Telefono",
                "area_progr": "Nombre"
            })
            df_renamed = df_renamed.dropna(subset=["lat", "lon"])

            comunas = sorted(df_renamed["Comuna"].dropna().unique().tolist())
            selector_comuna = pn.widgets.Select(name="Filtrar por comuna", options=["Todos"] + comunas, value="Todos", width=250)

            mapa_html = pn.pane.HTML("", min_height=500, sizing_mode="stretch_width")

            def generar_mapa(comuna):
                df_filtrado = df_renamed if comuna == "Todos" else df_renamed[df_renamed["Comuna"] == comuna]

                # Crear mapa centrado en el promedio de coordenadas
                lat_min, lat_max = df_filtrado["lat"].min(), df_filtrado["lat"].max()
                lon_min, lon_max = df_filtrado["lon"].min(), df_filtrado["lon"].max()
                centro = [(lat_min + lat_max) / 2, (lon_min + lon_max) / 2]

                mapa = folium.Map(
                    location=centro,
                    zoom_start=12,
                    control_scale=False,
                    zoom_control=False,  # oculta el control de zoom
                    scrollWheelZoom=False,  # desactiva zoom con scroll
                    dragging=False  # impide mover el mapa
                )

                # Agregar marcadores
                for _, row in df_filtrado.iterrows():
                    popup_html = f"""
                            <b>{row['Nombre']}</b><br>
                            {row['Barrio']} - {row['Comuna']}<br>
                            {row['Especialidad']}<br>
                            📞 {row['Telefono'] or 'No disponible'}
                            """
                    folium.Marker(
                        location=[row["lat"], row["lon"]],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.Icon(color="red", icon="plus-sign", prefix="fa")
                    ).add_to(mapa)

                # Renderizar mapa como HTML en Panel
                html = mapa._repr_html_().replace('height:100%;', 'height:500px;')
                mapa_html.object = html


        selector_comuna.param.watch(lambda event: generar_mapa(event.new), "value")
        generar_mapa("Todos")

        return pn.Column(
            pn.pane.Markdown("#### Mapa de Centros Médicos", sizing_mode="stretch_width"),
            selector_comuna,
            mapa_html,
            sizing_mode="stretch_width"
        )
