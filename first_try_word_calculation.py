import os
import fitz  # PyMuPDF
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
countries = ["USA", "FRANCE", "CHN", "UK", "RUS"]
years = ["2020", "2021", "2022", "2023", "2024"]  # Add 2024 when ready
keywords = ["sudan", "yemen", "syria", "south sudan", "somalia", "drc", "gaza"]

WORDS_PER_MINUTE = 100  # Adjust if you want a different speech pace

results = []

def analyze_speech(filepath, keywords):
    with fitz.open(filepath) as doc:
        text = " ".join([page.get_text() for page in doc]).lower()
    total_words = len(text.split())
    total_minutes = total_words / WORDS_PER_MINUTE

    keyword_counts = {kw: text.count(kw) for kw in keywords}
    keyword_ratios = {}
    keyword_times = {}

    for kw, count in keyword_counts.items():
        per_100 = (count / total_words * 100) if total_words > 0 else 0
        keyword_ratios[f"{kw} per 100 words"] = per_100
        keyword_times[f"{kw} minutes per mention"] = (total_minutes / count) if count > 0 else None

    return total_words, total_minutes, keyword_counts, keyword_ratios, keyword_times

# === Main Loop ===
for country in countries:
    for year in years:
        filename = f"{country} {year}.pdf"
        if not os.path.exists(filename):
            print(f"⚠️ Missing file: {filename}")
            continue

        total_words, total_minutes, keyword_counts, keyword_ratios, keyword_times = analyze_speech(filename, keywords)

        row = {
            "Country": country,
            "Year": year,
            "Total Words": total_words,
            "Estimated Minutes": round(total_minutes, 2)
        }
        for kw in keywords:
            row[f"{kw} (count)"] = keyword_counts[kw]
            row[f"{kw} per 100 words"] = keyword_ratios[f"{kw} per 100 words"]
            row[f"{kw} minutes per mention"] = keyword_times[f"{kw} minutes per mention"]
        results.append(row)

df = pd.DataFrame(results)
df.to_csv("p5_crisis_mentions_analysis.csv", index=False)
print(df)

# === Plot example for Sudan ===
kw = "sudan"  # Change to any keyword
per100_col = f"{kw} per 100 words"
minutes_col = f"{kw} minutes per mention"
count_col = f"{kw} (count)"

pivot_counts = df.pivot(index="Year", columns="Country", values=count_col).sort_index()
pivot_minutes = df.pivot(index="Year", columns="Country", values=minutes_col).sort_index()

x = np.arange(len(pivot_counts.index))
width = 0.12

fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar chart for raw counts
for i, country in enumerate(pivot_counts.columns):
    ax1.bar(x + (i - len(pivot_counts.columns)/2) * width + width/2,
            pivot_counts[country], width, label=f"{country} (count)")

ax1.set_ylabel("Mentions (Count)")
ax1.set_xlabel("Year")
ax1.set_xticks(x)
ax1.set_xticklabels(pivot_counts.index)
ax1.grid(axis='y', linestyle='--', alpha=0.6)

# Line chart for minutes per mention
ax2 = ax1.twinx()
for i, country in enumerate(pivot_minutes.columns):
    ax2.plot(x, pivot_minutes[country], marker='o', linestyle='-',
             label=f"{country} (min/mention)")

ax2.set_ylabel("Minutes per Mention")

fig.suptitle(f"Mentions of '{kw.title()}': Count vs Minutes per Mention", fontsize=14)
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left', fontsize=9)

plt.tight_layout()
plt.savefig(f"{kw.replace(' ', '_')}_mentions_minutes_chart.png")
plt.show()

