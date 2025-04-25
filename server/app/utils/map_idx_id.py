import pandas as pd

subset = pd.read_csv(r"D:\CollegeWork\ShopLens-AR-Shopping-Assistant\server\notebooks\subset_data.csv")


def map_idx_id(idx):
  return subset["article_id"].iloc[idx].tolist()