import pandas as pd
from transformers import pipeline
from tqdm import tqdm  # For progress bar

# Load the CSV files
clan_df = pd.read_csv('Data/clean_clan.csv')
id_df = pd.read_csv('Data/clean_id.csv')

# Select the pre-trained model for hate speech classification
classifier = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-hate-multiclass-latest")

# Function to determine if a term contains hate speech using the Hugging Face model
def classify_hate_speech(term):
    result = classifier(term)
    # Check if the label is any of the hate speech categories
    return result[0]['label'], result[0]['score']  # Returns the label and score

# Apply tqdm to monitor progress
tqdm.pandas()

# Apply the function to add a new column to clan_df with a progress bar
clan_df['hate_speech_label'], clan_df['confidence_score'] = zip(*clan_df['player_clan'].progress_apply(classify_hate_speech))

# Apply the function to add a new column to id_df with a progress bar
id_df['hate_speech_label'], id_df['confidence_score'] = zip(*id_df['player_id'].progress_apply(classify_hate_speech))

# Save the updated CSVs
clan_df.to_csv('Data/updated_clan.csv', index=False)
id_df.to_csv('Data/updated_id.csv', index=False)

print("Updated CSV files have been saved.")
