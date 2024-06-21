def clean_dataframe(df):

    df["an"] = df["ANMOIS"].str.slice(stop = 4)
    df["mois"] = df["ANMOIS"].str.slice(start = 4)

    # Remove leading zeros from 'mois' column
    df['mois'] = df['mois'].str.replace(r'^0+', '', regex=True)
    
    df.columns = [x.lower() for x in df.columns]

    return(df)