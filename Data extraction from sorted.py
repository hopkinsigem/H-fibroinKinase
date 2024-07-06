import re
import csv

# File paths
input_file_path = 'sorted_all_kinases_vs_atopsyche_davidsoni.out'
output_file_path = 'extracted_data.tsv'

# Initialize variables
query = ""
data_dict = {}
current_chromosome = ""
current_key = None
current_score = None
collecting = False

# Read the file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Process each line
for line in lines:
    # Extract Query
    query_match = re.match(r'^Query= (\S+)', line)
    if query_match:
        query = query_match.group(1)
    
    # Extract Chromosome and Score
    if line.startswith('>'):
        parts = line.split()
        current_chromosome = parts[0][1:]  # Remove '>' from chromosome name
        current_score = None  # Reset current_score for a new chromosome
        current_key = (query, current_chromosome)
        collecting = False
    
    # Extract Score
    score_match = re.match(r'\s*Score = ([\d.]+)', line)
    if score_match:
        current_score = float(score_match.group(1))
        current_key = (query, current_chromosome, current_score)  # Update key to include score
        collecting = True
    
    # Match Sbjct line with numerical values
    sbjct_match = re.match(r'^Sbjct\s+(\d+)\s+\S+\s+(\d+)', line)
    if sbjct_match and collecting:
        start_of_region = int(sbjct_match.group(1))
        end_of_region = int(sbjct_match.group(2))
        
        # Ensure start is the lower number and end is the higher number
        start_of_region, end_of_region = min(start_of_region, end_of_region), max(start_of_region, end_of_region)

        if current_key not in data_dict:
            data_dict[current_key] = [(start_of_region, end_of_region)]
        else:
            data_dict[current_key].append((start_of_region, end_of_region))

# Process the data to get the lowest start and highest end for each score block
final_data = []
for key, regions in data_dict.items():
    query, chromosome, score = key
    min_start = min(region[0] for region in regions)
    max_end = max(region[1] for region in regions)
    final_data.append([query, chromosome, min_start, max_end, score])

# Write the extracted data to a TSV file
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["Query", "Chromosome", "Start of Region", "End of Region", "Score"])
    writer.writerows(final_data)

print(f"Extracted data has been saved to {output_file_path}")