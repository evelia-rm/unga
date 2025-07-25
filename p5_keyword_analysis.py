import fitz  # PyMuPDF
import os
import pandas as pd
import matplotlib.pyplot as plt

# defining keywords to search, the countries, and the years
#keywords = ["climate change", "conflict", "extreme poverty"] 
keywords = [
    "syria",
    "yemen",
    "sudan",
    "south sudan",
    "somalia",
    "democratic republic of the congo",
    "gaza"
]

countries = ["USA", "CHN", "FRANCE", "RUS", "UK"]
years = [2017, 2018, 2019, 2020, 2021, 2022]

# intializing nested dictionary: {keyword -> {country -> {year -> count}}}
results = {
    keyword: {country: {str(year): 0 for year in years} for country in countries}
    for keyword in keywords
}

# analyzing each file
for country in countries:
    for year in years:
        filename = f"{country} {year}.pdf"
        if not os.path.exists(filename):
            print(f"Missing file: {filename}")
            continue

        with fitz.open(filename) as doc:
            text = ""
            for page in doc:
                text += page.get_text().lower()
            for keyword in keywords:
                results[keyword][country][str(year)] = text.count(keyword)

# Plotting each keyword across all countries
for keyword in keywords:
    df = pd.DataFrame(results[keyword])
    df.index.name = "Year"
    df = df.sort_index()

    plt.figure(figsize=(10, 6))
    for country in countries:
        plt.plot(df.index, df[country], marker='o', label=country)

    plt.title(f"P5 Mentions of '{keyword.title()}' (2017–2022)")
    plt.xlabel("Year")
    plt.ylabel("Mentions")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"p5_mentions_{keyword.replace(' ', '_')}.png")
    plt.show()