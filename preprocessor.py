import pandas as pd

def preprocess(df,region_df):
    # Merge with region_df
    df=df.merge(region_df,on="NOC",how="left")

    # Filtering for summer olympics 
    df=df[df["Season"]=="Summer"]

    # Removed Duplicate Values
    df.drop_duplicates(inplace=True)

    # One-hot-encoding medals
    df=pd.concat([df,pd.get_dummies(df["Medal"])],axis=1)
    df=df.loc[:, ~df.columns[::-1].duplicated()[::-1]]
    return df