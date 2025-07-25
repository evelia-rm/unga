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
    "2021": "USA 2021.pdf",
    "2022": "USA 2022.pdf",

    "2017": "CHN 2017.pdf",
    "2018": "CHN 2018.pdf",
    "2019": "CHN 2019.pdf",
    "2020": "CHN 2020.pdf",
    "2021": "CHN 2021.pdf",
    "2022": "CHN 2022.pdf", 

    "2017": "France 2017.pdf",
    "2018": "France 2018.pdf",
    "2019": "France 2019.pdf",
    "2020": "France 2020.pdf",
    "2021": "France 2021.pdf",
    "2022": "France 2022.pdf",

    "2017": "RUS 2017.pdf",
    "2018": "RUS 2018.pdf",
    "2019": "RUS 2019.pdf",
    "2020": "RUS 2020.pdf",
    "2021": "RUS 2021.pdf",
    "2022": "RUS 2022.pdf", 

    "2017": "UK 2017.pdf",
    "2018": "UK 2018.pdf",
    "2019": "UK 2019.pdf",
    "2020": "UK 2020.pdf",
    "2021": "UK 2021.pdf",
    "2022": "UK 2022.pdf"  
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
print("\nMentions of Key Topics (2017–2022):\n")
print(df)

# Plotting
plt.figure(figsize=(10, 6))
for kw in keywords:
    plt.plot(df.index, df[kw], marker='o', label=kw.title())

plt.title("Mentions by P5 in UN Speeches (2017–2022)")
plt.xlabel("Year")
plt.ylabel("Number of Mentions")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("p5_mentions_trend.png")
plt.show()