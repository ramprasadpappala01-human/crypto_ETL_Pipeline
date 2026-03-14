from sqlalchemy import create_engine
def load_data(df):
    engine=create_engine("postgresql://ram:1234@localhost:5432/rtcpp")
    df=df.rename(columns={"timestamp":"time_stamp"})
    print(df)
    df.to_sql("fact_crypto_prices",engine,if_exists="append",index=False)
    print("load completed")