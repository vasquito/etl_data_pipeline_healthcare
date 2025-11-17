import matplotlib
matplotlib.use("agg")

import panel as pn
import matplotlib.pyplot as plt
import seaborn as sns

class MedicalCentersGraph:
    def __init__(self, df):
        self.df = df

    def view(self):
        pn.extension()

        #df = find_all()
        df_renamed = self.df.rename(columns={
            "nombre": "Codigo",
            "barrio": "Barrio",
            "esp": "Especialidad",
            "comuna": "Comuna",
            "telefono": "Telefono",
            "area_progr": "Nombre"
        })

        #Tamaño uniforme
        figsize = (5.5, 3.5)
        plt.rcParams.update({
            "font.size": 8,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8
        })

        # 1. Centros por comuna
        fig1, ax1 = plt.subplots(figsize=figsize)
        comuna_counts = df_renamed["Comuna"].value_counts()
        sns.barplot(x=comuna_counts.values, y=comuna_counts.index, ax=ax1, color="steelblue")
        ax1.set_title("Centros por Comuna", fontsize=10)
        ax1.set_xlabel("Cantidad")
        ax1.set_ylabel("Comuna")
        plot1 = pn.pane.Matplotlib(fig1, tight=True)

        # 2. Distribución por especialidad
        fig2, ax2 = plt.subplots(figsize=figsize)
        esp_counts = df_renamed["Especialidad"].value_counts()
        ax2.pie(esp_counts.values, labels=esp_counts.index, autopct="%1.1f%%", startangle=90)
        ax2.set_title("Distribución por Especialidad", fontsize=10)
        plot2 = pn.pane.Matplotlib(fig2, tight=True)

        # 3. Centros por área programática
        fig3, ax3 = plt.subplots(figsize= figsize)
        area_counts = df_renamed["Nombre"].value_counts()
        sns.barplot(x=area_counts.values, y=area_counts.index, ax=ax3, color="steelblue")
        ax3.set_title("Centros por Área Programática", fontsize=10)
        ax3.set_ylabel("Cantidad")
        ax3.tick_params(axis='x', rotation=45)
        plot3 = pn.pane.Matplotlib(fig3, tight=True)

        return pn.GridBox(
            plot1, plot2, plot3,
            ncols=2,  # dos columnas
            sizing_mode="stretch_both"
        )
