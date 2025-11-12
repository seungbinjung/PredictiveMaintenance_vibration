"""
Parquet 파일에서 Label_No 열을 제거하고 저장하는 스크립트
"""
import pandas as pd
from pathlib import Path

# 파일 경로 설정
input_file = Path("test_dataset.parquet")
output_file = Path("no_label.parquet")

# Parquet 파일 로드
print(f"파일 로딩 중: {input_file}")
df = pd.read_parquet(input_file)

df = df.sample(frac=0.5).reset_index(drop=True)

print(f"원본 데이터 shape: {df.shape}")
print(f"컬럼 수: {len(df.columns)}")

# Label_No 열이 있는지 확인
if 'Label_No' in df.columns:
    print("Label_No 열 발견, 제거 중...")
    # Label_No 열 제거
    df_no_label = df.drop(columns=['Label_No'])
    print(f"Label_No 제거 후 shape: {df_no_label.shape}")
    print(f"컬럼 수: {len(df_no_label.columns)}")
else:
    print("Label_No 열이 없습니다. 원본 데이터를 그대로 사용합니다.")
    df_no_label = df

# 결과 저장
print(f"\n저장 중: {output_file}")
df_no_label.to_parquet(output_file, index=False)
print("저장 완료!")

# 확인
print(f"\n저장된 파일 정보:")
print(f"  - 파일: {output_file}")
print(f"  - 행 수: {len(df_no_label)}")
print(f"  - 컬럼 수: {len(df_no_label.columns)}")
print(f"  - 컬럼 목록 (처음 10개): {list(df_no_label.columns[:10])}")

