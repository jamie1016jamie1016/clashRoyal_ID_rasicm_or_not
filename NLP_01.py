import pandas as pd
from transformers import pipeline
from tqdm import tqdm  # For progress bar

# Load the CSV files
clan_df = pd.read_csv('Data/clean_clan.csv')
id_df = pd.read_csv('Data/clean_id.csv')

# Select a pre-trained model for offensive content detection
# Alternative models: "cardiffnlp/twitter-roberta-base-offensive" or "facebook/bart-large-mnli"
classifier = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-offensive")

# Function to determine if a term is offensive using the Hugging Face model
def is_offensive(term):
    result = classifier(term)
    # Check if the label is 'offensive' and the score is above a certain threshold
    return result[0]['label'] == 'LABEL_1' and result[0]['score'] > 0.7  # Adjust according to the model's label

# Apply tqdm to monitor progress
tqdm.pandas()

# Apply the function to add a new column to clan_df with a progress bar
clan_df['racist_or_not'] = clan_df['player_clan'].progress_apply(is_offensive)

# Apply the function to add a new column to id_df with a progress bar
id_df['racist_or_not'] = id_df['player_id'].progress_apply(is_offensive)

# Convert the boolean values to 'T' or 'F'
clan_df['racist_or_not'] = clan_df['racist_or_not'].apply(lambda x: 'T' if x else 'F')
id_df['racist_or_not'] = id_df['racist_or_not'].apply(lambda x: 'T' if x else 'F')

# Save the updated CSVs
clan_df.to_csv('Data/updated_clan.csv', index=False)
id_df.to_csv('Data/updated_id.csv', index=False)

print("Updated CSV files have been saved.")
