import fitz  # PyMuPDF
import os
import pandas as pd
import matplotlib.pyplot as plt

# Define keywords to search
keywords = ["climate change", "conflict", "extreme poverty"]

# Define years and associated filenames
files = {
    "2017": "USA 2017.pdf",
    "2018": "USA 2018.pdf",
    "2019": "USA 2019.pdf",
    "2020": "USA 2020.pdf",
    "2021": "USA 2021.pdf"
}

# Count keyword mentions
results = {year: {kw: 0 for kw in keywords} for year in files}

for year, filename in files.items():
    if not os.path.exists(filename):
        print(f"Missing: {filename}")
        continue
    with fitz.open(filename) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        for kw in keywords:
            results[year][kw] = text.lower().count(kw)

# Convert to DataFrame
df = pd.DataFrame.from_dict(results, orient="index")
print("\nMentions of Key Topics (2017–2021):\n")
print(df)

# Plotting
plt.figure(figsize=(10, 6))
for kw in keywords:
    plt.plot(df.index, df[kw], marker='o', label=kw.title())

plt.title("Mentions by USA in UN Speeches (2017–2021)")
plt.xlabel("Year")
plt.ylabel("Number of Mentions")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("usa_mentions_trend.png")
plt.show()