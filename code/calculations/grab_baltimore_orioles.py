import pandas as pd
from win_loss_utils import c3_argmax_n2_fast
import ast

master = pd.read_csv('../../output/csvs/master_database.csv')

balt2002 = master[(master['team'] == "Baltimore Orioles") & (master['season'] == 2002)]

balt2002['sequence_numeric'] = balt2002['sequence'].apply(ast.literal_eval)

seq = balt2002['sequence_numeric'].iloc[0]

args = c3_argmax_n2_fast(seq, N=1000000)

print(f"Baltimore Orioles 2002 — n3*: {args[0]}, c3*: {args[1]:.4f}")