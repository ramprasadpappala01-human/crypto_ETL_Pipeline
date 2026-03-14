from sqlalchemy import create_engine
import pandas as pd
def load_data(df):
    engine=create_engine("postgresql://ram:1234@localhost:5432/rtcpp")
    coin_dim=pd.read_sql("SELECT coin_id , coin_name FROM coin_dim",engine)
    date_dim=pd.read_sql("SELECT full_date , date_id FROM date_dim",engine)
    df=df.merge(coin_dim,on="coin_name",how="left")

    df["time_stamp"] = pd.to_datetime(df["time_stamp"])
    df['full_date']=df['time_stamp'].dt.date
    date_dim["full_date"] = pd.to_datetime(date_dim["full_date"]).dt.date
    # print(df['full_date'])
    new_dates=set(df['time_stamp'])-set(date_dim['full_date'])
    if new_dates:
        new_df=pd.DataFrame({"full_date":list(new_dates)})
        new_df['year']=new_df['full_date'].dt.year
        new_df['month']=new_df['full_date'].dt.month
        new_df['day']=new_df['full_date'].dt.day
        new_df.to_sql("date_dim",engine,if_exists='append',index=False)
        date_dim=pd.read_sql("SELECT full_date , date_id FROM date_dim",engine)
    df=df.merge(date_dim,on="full_date",how='left')
    fact_df=df[['coin_id','date_id','price']]
    print(fact_df)
    print(set(df["full_date"]) - set(date_dim["full_date"]))
    fact_df.to_sql("fact_crypto_prices",engine,if_exists="append",index=False)
    print("load completed")