import os
import fitz  # PyMuPDF
import matplotlib.pyplot as plt

# === CONFIG ===
country = "CHN"               # change the country selected
years = range(2017, 2025)     # year range 

# === Word count storage ===
word_counts = {}

for year in years:
    filename = f"{country} {year}.pdf"
    if not os.path.exists(filename):
        print(f"⚠️ Missing file: {filename}")
        continue

    with fitz.open(filename) as doc:
        text = " ".join([page.get_text() for page in doc])
    word_counts[year] = len(text.split())

# === Print results ===
for year, count in word_counts.items():
    print(f"{country} {year}: {count} words")

# === Plot ===
plt.figure(figsize=(8, 5))
plt.bar(word_counts.keys(), word_counts.values(), color="skyblue")
plt.title(f"Word Count for {country} UNGA Speeches ({min(years)}–{max(years)})")
plt.xlabel("Year")
plt.ylabel("Word Count")
plt.xticks(list(word_counts.keys()))
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(f"{country}_word_count_chart.png")
plt.show()
