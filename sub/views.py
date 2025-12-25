import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import json


def find_column(key_group, df_columns):
    keys = key_group if isinstance(key_group, tuple) else (key_group,)
    for key in keys:
        for col in df_columns:
            if key in col:
                return col
    return None


# 다운로드 시 바코드 패턴 기반으로 행 자동 제거함수
def trim_rows_by_barcode_pattern(df):
    if '바코드' not in df.columns:
        return df

    barcode = df['바코드'].astype(str)
    valid_pattern = r'^[A-Za-z][0-9A-Za-z]+$'
    invalid_index = barcode[~barcode.str.match(valid_pattern)].index

    if len(invalid_index) > 0:
        cut = invalid_index[0]
        df = df.loc[:cut - 1]

    return df


def index(request):
    if request.method == 'POST':
    # Download Request
        if request.POST.get('data') and request.POST.get('columns'):
            data = json.loads(request.POST.get('data'))
            columns = json.loads(request.POST.get('columns'))

            df = pd.DataFrame(data, columns=columns).fillna('')

            # 시스템 위치 합치기, z좌표 소수점 제거
            if '변경위치' in df.columns and ('Z좌표' in df.columns or 'Z 좌표' in df.columns):
                z_col = 'Z좌표' if 'Z좌표' in df.columns else 'Z 좌표'
                df[z_col] = df[z_col].astype(str).apply(
                    lambda x: x[:-2] if x.endswith('.0') else x
                )
                df['시스템 위치'] = df['변경위치'].astype(str) + '-' + df[z_col].astype(str)
                df = df.drop(columns=['변경위치', z_col])

            # Column Mapping
            column_map = {
                '바코드': '바코드',
                '변경호스트': '호스트명',
                'MAC_ADDRESS': 'MAC',
                ('변경IP', '변경 IP', '공인IP', '공인 IP'): 'Primary IP',
                ('변경IPMI', '변경 IPMI'): '관리 IP',
                '시스템 위치': '시스템 위치',
            }

            all_headers = [
                '바코드', '호스트명', '서비스닉', 'OS', 'MAC', '도메인',
                'Primary IP', 'Other_IP', '관리 IP',
                '시스템 위치',
                'C', 'I', 'DKOS PM 리전', '비고', 'ITGC 여부'
            ]

            out_df = pd.DataFrame(columns=all_headers)

            for k, v in column_map.items():
                source_col = find_column(k, df.columns)
                out_df[v] = df[source_col] if source_col else ''

            out_df.fillna('', inplace=True)

            # 호스트명 'x' , 'X' 만 공백 처리
            if '호스트명' in out_df.columns:
                out_df['호스트명'] = out_df['호스트명'].astype(str)
                out_df.loc[out_df['호스트명'].str.strip().isin(['x', 'X']), '호스트명'] = ''

            # 다운로드 시 바코드 패턴 기반 제거
            out_df = trim_rows_by_barcode_pattern(out_df)

            # Make Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                out_df.to_excel(writer, sheet_name='Sheet1', index=False)

            output.seek(0)
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="server_update_form.xlsx"'
            return response

    # File Upload Part
        uploaded_files = request.FILES.getlist('excel_file')
        files_data = []

        start_keys = ["바코드", "호스트명"]

        for excel_file in uploaded_files:
            df_raw = pd.read_excel(excel_file, header=None)

            # Find Header Column
            header_row_idx = None
            for idx, row in df_raw.iterrows():
                if row.astype(str).str.contains("|".join(start_keys)).any():
                    header_row_idx = idx
                    break

            if header_row_idx is None:
                continue

            headers = df_raw.iloc[header_row_idx].fillna('').astype(str).str.strip().tolist()
            df = df_raw.iloc[header_row_idx + 1:].copy()
            df.columns = headers

            # Start Column auto Searching
            start_idx = None
            for key in start_keys:
                if key in headers:
                    idx = headers.index(key)
                    if start_idx is None or idx < start_idx:
                        start_idx = idx

            if start_idx is None:
                continue

            # End Column Expansion
            end_idx = len(headers) - 1

            df = df[headers[start_idx:end_idx + 1]]
            df = df.fillna('')

            files_data.append({
                'name': excel_file.name,
                'headers': df.columns.tolist(),
                'table_data': df.values.tolist(),
            })

        return render(request, 'sub/index.html', {'files_data': json.dumps(files_data)})

    return render(request, 'sub/index.html')

