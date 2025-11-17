import panel as pn

class MedicalCentersTable:
    def __init__(self, df):
        self.df = df

    def view(self):
        pn.extension('tabulator')
        df_renamed = self.df.rename(columns={
            "nombre": "Codigo",
            "barrio": "Barrio",
            "esp": "Especialidad",
            "comuna": "Comuna",
            "telefono": "Telefono",
            "area_progr": "Nombre"
        })

        # Columnas visibles
        columnas = ["Codigo", "Nombre", "Barrio", "Comuna", "Especialidad", "Telefono"]

        # Filtro externo
        comunas = sorted(df_renamed["Comuna"].dropna().unique().tolist())
        comuna_selector = pn.widgets.Select(
            name="Filtrar por comuna",
            options= ["Todos"] + comunas,
            value="Todos",
            width=250
        )

        tabla = pn.widgets.Tabulator(
            df_renamed[columnas],
            pagination="local",
            page_size=10,
            layout="fit_data_fill",
            show_index=False,
            sizing_mode="stretch_width",
            configuration={"header_filters": True}
        )

        def actualizar_tabla(event):
            comuna = comuna_selector.value
            if comuna != "Todos":
                df_filtrado = df_renamed[df_renamed["Comuna"] == comuna]
            else:
                df_filtrado = df_renamed
            tabla.value = df_filtrado[columnas]
        comuna_selector.param.watch(actualizar_tabla, "value")

        # Button export
        button_export = pn.widgets.Button(name="Exportar CSV", button_type="primary", width=150)
        def exportar_csv(event):
            tabla.download("centros_medicos.csv")
        button_export.on_click(exportar_csv)


        return pn.Column(
            pn.pane.Markdown("#### Centros Médicos Barriales", sizing_mode="stretch_width"),
            pn.Column(
            pn.Row(
                pn.Column(comuna_selector, sizing_mode="stretch_width"),
                        pn.Column(button_export, sizing_mode="stretch_width")
                    ),
                    pn.Row(
                        pn.Column(tabla, sizing_mode="stretch_width")
                    )
            ), sizing_mode="stretch_width"
        )
