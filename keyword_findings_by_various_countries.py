import os
import fitz  # PyMuPDF
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# settings 
countries = ["USA", "FRANCE", "CHN", "UK", "RUS"]
years = ["2017", "2019", "2021", "2022"]
keywords = ["climate change"]  # You can change this to conflict, gaza, etc.

# data countainer 
data = {country: [] for country in countries}

# analyzing the pdfs 
for country in countries:
    for year in years:
        filename = f"{country} {year}.pdf"
        if not os.path.exists(filename):
            print(f" Missing: {filename}")
            data[country].append(0)
            continue
        text = ""
        with fitz.open(filename) as doc:
            for page in doc:
                text += page.get_text().lower()
        count = sum(text.count(k) for k in keywords)
        data[country].append(count)

# plot grouped by bar chart 
x = np.arange(len(years))  # the label locations
width = 0.15  # width of the bars

fig, ax = plt.subplots(figsize=(12, 6))

for i, (country, counts) in enumerate(data.items()):
    offset = (i - len(countries)/2) * width + width/2
    ax.bar(x + offset, counts, width, label=country)

# labels and formatting
ax.set_ylabel('Mentions')
ax.set_title(f"Mentions of '{', '.join(keywords)}' by P5 Countries")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# save and show
plt.savefig("p5_keyword_comparison_bar.png")
plt.show()
