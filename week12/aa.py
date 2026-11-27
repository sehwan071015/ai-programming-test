import pandas as pd
df = pd.read_csv("scores_2026.csv")
print(df.shape)

df = pd.read_csv("scores_2026.csv")
df.shape # (114, 5)
df["점수"].isna().sum() # 6 ← 빈 칸이 몇 개인가
df.duplicated().sum() # 4 ← 완전히 같은 행이 몇 개인가
df["반"].unique() # ['2반' '1반' '1반 '] ← 세 개?
df["과목"].unique() # ['수학' '프로그래밍' '영어' '프로그래밍 ']
df["점수"].describe() # max 999.0 min -5.0 ← 점수인데?

df = pd.read_csv("scores_2026_cp949.csv")
