import pandas as pd

assets = pd.read_csv("tests/ames_train_cleaned.csv")
assets["is_new"] = assets["Year_Built"] > 1970
