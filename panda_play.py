
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_rno = pd.read_csv("data/rno.gff3", delimiter='\t', comment="#")


print("read <" + str(len(df_rno)) + "> lines")

# Set the column names
df_rno.columns =['feature', 'empty1', "type", 'start', 'stop', 'empty2', 'strand', 'empty3', 'attributes']

#Check the column names
list(df_rno.columns.values)

# list the first 3 rows
df_rno.head(3)

# Get the rows containing miRNA_primary_transcript entries
df_hairpins = df_rno[df_rno["type"]=="miRNA_primary_transcript"]

# how many miRNA_primary_transcripts ?

# get primary transcripts on chr1
df_hairpins_chr1 = df_hairpins[df_hairpins['feature']=='chr1']


df_rno['len'] = df_rno['stop'] - df_rno['start'] + 1
w=10
plt.figure(figsize=(10, 6))
sns.histplot(data=df_rno, x='len', kde=True, bins = np.linspace(0, 200, 20), color='blue', edgecolor='slateblue')
plt.title('feature length distribution')
plt.xlabel('length (nt)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig("rno.png")
plt.show()

print("done")




# see here for a list of colour names
# https://matplotlib.org/stable/gallery/color/named_colors.html