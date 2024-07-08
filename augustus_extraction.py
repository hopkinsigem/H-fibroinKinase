
import pandas as pd

# Load the gene regions from augustusgenes.csv
genes_df = pd.read_csv('augustusgenes.csv')

# Load the kinase regions from extracted_data.tsv
kinase_df = pd.read_csv("extracted_data.tsv", sep='\t')

# Merge the dataframes on the Chromosome column
merged_df = pd.merge(genes_df, kinase_df, on='Chromosome')

#merged_df.to_csv('merged.csv', index=False)

# Filter the merged dataframe to find kinase regions within gene regions
filtered_df = merged_df[(merged_df['Start_y'] >= merged_df['Start_x']) & 
                        (merged_df['End_y'] <= merged_df['End_x'])]

# Select relevant columns and rename them for clarity
results_df = filtered_df[['Attribute', 'Start_x', 'End_x', 'Chromosome', 'Start_y', 'End_y', 'Query']]
results_df.columns = ['gene_id', 'gene_start', 'gene_end', 'kinase_chromosome', 'kinase_start', 'kinase_end', 'kinase_query']

# Save the results to a CSV file
results_df.to_csv('kinase_within_genes.csv', index=False)

print("Results saved to 'kinase_within_genes.csv'")
