import sweetviz as sv
import pandas as pd

df = pd.read_csv("exemplo.csv")

analise = sv.analyze(df)

analise.show_html("analise.html")
