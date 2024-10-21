# Clash Royale Data Scraper and Offensive Content Classifier

## Overview
This project scrapes data from the Clash Royale leaderboard (via a third-party website), processes the scraped data, and applies natural language processing (NLP) models to detect offensive or racist content within player IDs and clan names.

The project contains multiple scripts for web scraping, data cleaning, and classification. It follows the below workflow:
1. Scraping player data (IDs and clan names).
2. Cleaning the scraped data by removing non-English characters, duplicates, and punctuation.
3. Using pre-trained NLP models to classify offensive content.

## Project Structure

- **scrap_data.py**: This script scrapes data from the Clash Royale leaderboard using Selenium. The script navigates the webpage, collects player data (ID and clan name), and saves it into CSV files.
  
- **clean_clan.ipynb** & **clean_id.ipynb**: These Jupyter notebooks clean and preprocess the scraped data by:
  - Removing non-English characters.
  - Removing duplicates to ensure each clan name and player ID is unique.
  - Removing punctuation marks in player IDs and clan names.
  After cleaning, the data is saved into separate CSV files (`clean_clan.csv` and `clean_id.csv`).

- **NLP_01.py** & **NLP_02.py**: These Python scripts load the cleaned CSV files and apply two different NLP models using the Hugging Face transformers library. They classify whether the player ID or clan name contains offensive or racist content. 
    - `NLP_01.py`: Uses the `"cardiffnlp/twitter-roberta-base-offensive"` model to detect offensive language.
    - `NLP_02.py`: Uses the `"cardiffnlp/twitter-roberta-base-hate-multiclass-latest"` model to detect hate speech.

## Installation

To run this project, you need the following libraries installed:

```bash
pip install selenium pandas transformers tqdm
```

Additionally, you need to have [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed and available in your system's PATH for web scraping.

## How to Use

1. **Scrape Data:**
   - Run the `scrap_data.py` script to collect player IDs and clan names from the Clash Royale leaderboard. The script will save the data into CSV files.

2. **Clean Data:**
   - Use `clean_clan.ipynb` and `clean_id.ipynb` to clean and split the scraped data into two separate CSV files: `clean_clan.csv` for clan names and `clean_id.csv` for player IDs. These scripts will remove non-English characters, duplicates, and punctuation.

3. **Classify Offensive Content:**
   - Run `NLP_01.py` to classify whether the player ID or clan name contains offensive language.
   - Run `NLP_02.py` to classify whether the player ID or clan name contains hate speech.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Hugging Face**: For providing pre-trained NLP models.
- **Selenium**: For web scraping tools.
- **Clash Royale**: This project is not affiliated with or endorsed by Clash Royale or Supercell.

## Future Work

- Enhance the scraping process to collect more data points.
- Explore additional models for classification.
- Automate the workflow using a pipeline tool such as Apache Airflow.
