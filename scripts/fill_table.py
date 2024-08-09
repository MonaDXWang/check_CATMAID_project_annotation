import os
import pandas as pd
import re
from util import nclass, clean_name

# Function to preprocess and merge columns with the same cell pairs
def preprocess_connectivity_data(df):
    df = df.copy()
    standardized_columns = {}
    for col in df.columns:
        if col.startswith('#Synapses with '):
            partner = col.replace('#Synapses with ', '')
            cleaned_partner = clean_name(partner)
            standardized_partner = nclass(cleaned_partner)
            standardized_columns.setdefault(standardized_partner, []).append(col)
    
    for partner, cols in standardized_columns.items():
        if len(cols) > 1:
            df[f'#Synapses with {partner}'] = df[cols].sum(axis=1)
            df.drop(columns=cols, inplace=True)
    return df

# Function to determine the update column based on the filename
def determine_update_column(filename, criteria_columns):
    for criteria, column_name in criteria_columns.items():
        if criteria in filename:
            return column_name
    return None

# Function to check and update the curation DataFrame
def update_curation(row, connectivity_pairs, cells_in_synapses):
    neuron = nclass(clean_name(row['Neuron']))
    partner = nclass(clean_name(row['Partner']))
    if (neuron, partner) in connectivity_pairs or (partner, neuron) in connectivity_pairs:
        return "Yes"
    elif neuron in cells_in_synapses or partner in cells_in_synapses:
        return "No"
    else:
        return ""

# Paths and criteria
input_folder_path = './input/connectivity/'
output_path = './output/merged_updated_neuron_connections_table.csv'

# Criteria and corresponding columns
criteria_columns = {
    "conf_all": 'Mona conf (all)',
    "threshold_4": 'Dauer_2 (Mona) conf >=4'
}

# Load the main table that needs to be filled
main_table_path = './input/Gap_junction_curation.csv'
main_table = pd.read_csv(main_table_path)

# Process the "conf all" table first
conf_all_filepath = None
for filename in os.listdir(input_folder_path):
    if "conf_all" in filename and filename.endswith(".csv"):
        conf_all_filepath = os.path.join(input_folder_path, filename)
        break

if conf_all_filepath:
    big_csv = pd.read_csv(conf_all_filepath)
    big_csv = preprocess_connectivity_data(big_csv)
    
    connectivity_pairs = set()
    cells_in_synapses = set()

    for index, row in big_csv.iterrows():
        neuron = row['Gap junction with neuron']
        if neuron != 'ALL (257 neurons)':  # Skipping the summary row
            for col in big_csv.columns:
                if col.startswith('#Synapses with') and row[col] > 0:
                    partner = col.replace('#Synapses with ', '').strip()
                    clean_partner = nclass(clean_name(partner))
                    clean_neuron = nclass(clean_name(neuron))
                    connectivity_pairs.add((clean_neuron, clean_partner))
                    connectivity_pairs.add((clean_partner, clean_neuron))
                    cells_in_synapses.add(clean_partner)

    # Add new connections from "conf all" table to main table
    new_rows = []
    conf_all_column = criteria_columns["conf_all"]
    for (neuron, partner) in connectivity_pairs:
        if not ((main_table['Neuron'] == neuron) & (main_table['Partner'] == partner)).any() and not ((main_table['Neuron'] == partner) & (main_table['Partner'] == neuron)).any():
            new_rows.append({'Neuron': neuron, 'Partner': partner, conf_all_column: 'Yes'})
    
    new_rows_df = pd.DataFrame(new_rows)
    main_table = pd.concat([main_table, new_rows_df], ignore_index=True)

    # Update the "conf_all" column for existing rows
    main_table[conf_all_column] = main_table.apply(lambda row: 'Yes' if ((nclass(clean_name(row['Neuron'])), nclass(clean_name(row['Partner']))) in connectivity_pairs or (nclass(clean_name(row['Partner'])), nclass(clean_name(row['Neuron']))) in connectivity_pairs) else ('No' if (nclass(clean_name(row['Neuron'])) in cells_in_synapses or nclass(clean_name(row['Partner'])) in cells_in_synapses) else row.get(conf_all_column, '')), axis=1)
# Process the remaining files
for filename in os.listdir(input_folder_path):
    if filename.endswith(".csv") and "conf_all" not in filename:
        filepath = os.path.join(input_folder_path, filename)
        big_csv = pd.read_csv(filepath)
        
        # Preprocess the big CSV file to merge columns with the same cell pairs
        big_csv = preprocess_connectivity_data(big_csv)

        # Extract the connections from the connectivity DataFrame
        connectivity_pairs = set()
        cells_in_synapses = set()

        for index, row in big_csv.iterrows():
            neuron = row['Gap junction with neuron']
            if neuron != 'ALL (257 neurons)':  # Skipping the summary row
                for col in big_csv.columns:
                    if col.startswith('#Synapses with') and row[col] > 0:
                        partner = col.replace('#Synapses with ', '').strip()
                        clean_partner = nclass(clean_name(partner))
                        clean_neuron = nclass(clean_name(neuron))
                        connectivity_pairs.add((clean_neuron, clean_partner))
                        connectivity_pairs.add((clean_partner, clean_neuron))
                        cells_in_synapses.add(clean_partner)

        # Determine the update column based on the filename
        update_column = determine_update_column(filename, criteria_columns)
        if not update_column:
            continue

        # Apply the function to update the specified column
        main_table[update_column] = main_table.apply(lambda row: update_curation(row, connectivity_pairs, cells_in_synapses), axis=1)


# Order main_table first by Neuron and then by Partner alphabetically within each Neuron
main_table = main_table.sort_values(by=['Neuron', 'Partner'])

# Save the updated main table to a new CSV file
main_table.to_csv(output_path, index=False)

# Print the number of 'Yes' values in each update column
yes_counts = {col: main_table[col].value_counts().get("Yes", 0) for col in criteria_columns.values()}
print(f"Number of Yes values: {yes_counts}")

print(f"Table has been updated and saved to '{output_path}'.")

