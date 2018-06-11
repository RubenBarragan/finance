import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

stocks = [
  "FB", 
  "TWTR",
  "MSFT",
  "NVDA",
  "PANW"
]

def main():
  print(compute_total_comulative_year())
  plot_all()

def compute_total_comulative_year():
  data = []
  for stock in stocks:
    data.append(compute_table("csv/" + stock + ".csv")["Total"].iloc[-1])
  columns = ["Returns Over 12 Months"]
  return pd.DataFrame(data, stocks, columns)

def plot_all():
  column = "Adj Close"
  data = []
  for stock in stocks:
    data.append(compute_table("csv/" + stock + ".csv"))
  plt.grid(True)
  for dt in data:
    plt.plot(dt[["Adj Close"]])
  plt.xticks(range(0,len(data[0]["Date"])), data[0]["Date"], rotation='vertical')
  plt.tight_layout()
  plt.legend(stocks)
  plt.show()

def plot(name, df, column):
  print(df)
  plt.plot(df[column])
  plt.grid(True)
  plt.xticks(range(0,len(df)), df['Date'], rotation='vertical')
  plt.tight_layout()
  plt.legend([name])
  plt.show()

def compute_table(csv_path):
  df = pd.read_csv(csv_path)

  comulative_return = [None]
  gross_return = [None]
  total_gross_comulative_return = [1]
  total_comulative_return = [1]
  
  for i in range(1, len(df)):
    comulative_return.append((df.T[i]["Adj Close"] - df.T[i-1]["Open"]) / df.T[i-1]["Open"])
    gross_return.append(comulative_return[-1] + 1)
    total_gross_comulative_return.append(total_gross_comulative_return[-1] * gross_return[-1])
    total_comulative_return.append(total_gross_comulative_return[-1] - 1)
  
  comulative_return_serie = pd.Series(comulative_return)
  total_comulative_return_serie = pd.Series(total_comulative_return)
  df = df.assign(Comulative=comulative_return_serie)
  df = df.assign(Total=total_comulative_return_serie)
  return df

if __name__ == "__main__":
  main()