import pandas as pd

def add_to_master(new_word, csv_file="master_parts.csv"):
    df = pd.read_csv(csv_file)

    # check if word already exists (case-insensitive)
    if new_word.lower() not in df["part_name"].str.lower().values:
        df = pd.concat([df, pd.DataFrame({"part_name": [new_word]})], ignore_index=True)
        df.to_csv(csv_file, index=False)
        return True
    return False