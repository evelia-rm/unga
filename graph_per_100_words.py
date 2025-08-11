import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
csv_file = "p5_keyword_time_analysis.csv"  # from previous analysis script
keywords = ["climate change", "conflict", "extreme poverty"]

# === Load Data ===
df = pd.read_csv(csv_file)

# === Plot for each keyword ===
for kw in keywords:
    # --- Chart 1: Mentions per 100 words ---
    per100_col = f"{kw} per 100 words"
    if per100_col not in df.columns:
        print(f"⚠️ Column {per100_col} not found, skipping keyword {kw}")
        continue

    pivot_per100 = df.pivot(index="Year", columns="Country", values=per100_col)
    pivot_per100 = pivot_per100.sort_index()

    x = np.arange(len(pivot_per100.index))
    width = 0.15

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, country in enumerate(pivot_per100.columns):
        ax.bar(x + (i - len(pivot_per100.columns)/2) * width + width/2,
               pivot_per100[country], width, label=country)

    ax.set_title(f"Mentions of '{kw.title()}' per 100 Words (P5 Countries)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Mentions per 100 Words")
    ax.set_xticks(x)
    ax.set_xticklabels(pivot_per100.index)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{kw.replace(' ', '_')}_per100words.png")
    plt.show()

    # --- Chart 2: Minutes per Mention ---
    minutes_col = f"{kw} minutes per mention"
    if minutes_col not in df.columns:
        print(f"⚠️ Column {minutes_col} not found, skipping minutes chart for {kw}")
        continue

    pivot_minutes = df.pivot(index="Year", columns="Country", values=minutes_col)
    pivot_minutes = pivot_minutes.sort_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, country in enumerate(pivot_minutes.columns):
        ax.bar(x + (i - len(pivot_minutes.columns)/2) * width + width/2,
               pivot_minutes[country], width, label=country)

    ax.set_title(f"Minutes per Mention of '{kw.title()}' (P5 Countries)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Minutes per Mention")
    ax.set_xticks(x)
    ax.set_xticklabels(pivot_minutes.index)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{kw.replace(' ', '_')}_minutes_per_mention.png")
    plt.show()
