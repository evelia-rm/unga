import fitz  
import matplotlib.pyplot as plt

# configuration
country = "USA"          # Options: FRANCE, USA, UK, RUS, CHN
year1 = "2023"
year2 = "2024"

# keywords to compare
keywords = [
    "syria", 
    "yemen", 
    "sudan", 
    "south sudan", 
    "somalia", 
    "drc", 
    "gaza"
]

# File names
file1 = f"{country.upper()} {year1}.pdf"
file2 = f"{country.upper()} {year2}.pdf"

# === text extraction and counting ===
def extract_text(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text().lower()
    return text

def count_mentions(text, keywords):
    return {kw: text.count(kw) for kw in keywords}

# read and analyze both files
text1 = extract_text(file1)
text2 = extract_text(file2)
counts1 = count_mentions(text1, keywords)
counts2 = count_mentions(text2, keywords)

# table output
print(f"\n🔍 Keyword Comparison for {country.upper()} ({year1} vs {year2}):\n")
print(f"{'Keyword':<20} {year1:>8} {year2:>8}")
print("-" * 38)
for kw in keywords:
    print(f"{kw:<20} {counts1[kw]:>8} {counts2[kw]:>8}")

# bar chart
labels = keywords
x = range(len(labels))

plt.figure(figsize=(12, 6))
plt.bar([i - 0.2 for i in x], [counts1[k] for k in labels], width=0.4, label=year1)
plt.bar([i + 0.2 for i in x], [counts2[k] for k in labels], width=0.4, label=year2)

plt.xticks(x, labels, rotation=45, ha='right')
plt.ylabel("Mentions")
plt.title(f"{country.upper()} Speech Comparison ({year1} vs {year2})")
plt.legend()
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig(f"{country.lower()}_comparison_{year1}_{year2}.png")
plt.show()
