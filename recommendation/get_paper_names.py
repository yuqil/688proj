import config
import pandas as pd
import os


paper_df = pd.read_csv(os.path.join(config.base_csv_dir, 'paper.csv'))
fout = open('papers.txt', 'w')
for index, row in paper_df.iterrows():
    try:
        fout.write(row['title'] + '\n')
    except:
        continue
fout.close()