import pandas as pd

def create_data_from_input(df, annee, mois):
    mois = str(mois)
    data = df.query("an == @annee").query("mois == @mois")
    return(data)

def summary_stat_airport(data):
    table2 = (
        data
        .groupby(["apt", "apt_nom"])
        .agg({"apt_pax_dep": "sum", "apt_pax_arr": "sum", "apt_pax_tr": "sum", "trafic": "sum"})
        .sort_values("trafic", ascending=False)
        .reset_index()
    )
    table2.columns = table2.columns.str.replace("apt_pax_", "pax")
    return table2
