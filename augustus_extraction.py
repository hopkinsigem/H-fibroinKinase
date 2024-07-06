
import pandas as pd
import pyranges as pr

file_path = "Galaxy35-[Augustus_on_data_34__GTF_GFF].gtf"
# Read the GTF file into a pandas DataFrame
# The GTF file is tab-separated and may contain comment lines starting with '#'
gtf_df = pd.read_csv(file_path, sep='\t', comment='#', header=None)
data_df = pd.read_csv("extracted_data.tsv", sep='\t')

# Rename the columns for easier reference
gtf_df.columns = ['Chromosome', 'Source', 'Feature', 'Start', 'End', 'Score', 'Strand', 'Frame', 'Attribute']

# Filter the DataFrame to show only entries with the feature type "gene" and sort data_df to be in order of Chromosome number
gene_df = gtf_df[gtf_df['Feature'] == 'gene']
data_df = data_df.sort_values('Chromosome')
#Remove extra columns from the gene_df (don't need them to find overlaps)
gene_df = gene_df.drop(columns=['Score', 'Strand', 'Frame', 'Feature', 'Source'])

# Display the first few rows of the filtered dataframe
print(gene_df)
print(data_df)
# Convert DataFrames to PyRanges objects
augustusgenes_gr = pr.PyRanges(gene_df)
extracted_data_gr = pr.PyRanges(data_df)

# Find overlapping regions
overlaps = augustusgenes_gr.join(extracted_data_gr)

# Convert the result back to a pandas DataFrame
overlaps_df = overlaps.df
#Gene = gene areas predicted by Augustus
overlaps_df.rename(columns={'Start': 'Gene Start', 'End': 'Gene End', 'Start_b': 'Kinase Start', 'End_b': 'Kinase End'}, inplace=True)

print("\nOverlapping Regions DataFrame:")
print(overlaps_df)

# Optionally, save the overlaps to a CSV file
overlaps_df.to_csv('overlapping_regions.csv', index=False)