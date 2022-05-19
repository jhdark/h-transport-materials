from pyparsing import col
import h_transport_materials as htm
import pandas as pd
import numpy as np
import plotly.express as px

diffusivities = htm.diffusivities.filter(material="tungsten")
data = []
for D in diffusivities:
    label = "{} {} ({})".format(D.isotope, D.author.capitalize(), D.year)
    range = D.range
    if D.range is None:
        range = (300, 1200)
    for T in np.linspace(range[0], range[1], num=50):
        data.append(
            [1 / T, D.value(T), label]  # , D.isotope, D.year, D.author.capitalize()
        )

df = pd.DataFrame(
    np.array(data), columns=["x", "y", "label"]
)  # , "isotope", "year", "author"
fig = px.line(df, x="x", y="y", color="label")

fig.show()
