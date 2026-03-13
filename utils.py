import pandas as pd 
import json

def save_to_csv(data, filename):
    # convert the data to a dataframe
    df = pd.DataFrame(data)
    # save to a csv file 
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename} as a CSV file 📂")

def save_to_json(data, filename):
    # write into the file 
    with open (filename, "w") as f :
        # save file to json
        json.dump(data, f, indent=4)
    print(f"Data successfully saved to {filename} as a JSON file 🗃️")
