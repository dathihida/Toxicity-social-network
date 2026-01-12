import pandas as pd
import matplotlib.pyplot as plt

import os

out_path_dir = "../output"
os.makedirs(out_path_dir, exist_ok=True)

df = pd.read_excel("../result_test.xlsx")

true_col = "Toxicity"
pred_col = "predicted_label"

df["is_correct"] = df[true_col] == df[pred_col]

correct = df["is_correct"].sum()
incorrect = len(df) - correct

plt.figure()
plt.bar(["Correct", "Incorrect"], [correct, incorrect])
plt.title("Prediction Result Comparison")
plt.xlabel("Result")
plt.ylabel("Number of samples")
plt.show()

wrong_df = df[df["is_correct"] == False][
    ["Comment", "Toxicity", "predicted_label"]
]
print("Wrong Predictions:")
print(wrong_df)

wrong_df.to_excel(
    os.path.join(out_path_dir, "wrong_predictions_phobert.xlsx"),
    index=False
)

same_rate = (df["Toxicity"] == df["predicted_label"]).mean() * 100
print(f"Tỉ lệ giống nhau: {same_rate:.2f}%")