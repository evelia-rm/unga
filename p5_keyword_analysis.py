import fitz  # PyMuPDF
import os
import pandas as pd
import matplotlib.pyplot as plt

# defining years and associated filenames
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

# defining keywords to search, the countries, and the years
keywords = ["climate change", "conflict", "extreme poverty"]
countries = ["USA", "CHINA", "FRANCE", "RUSSIA", "UK"]
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