import pandas as pd

def process_excel(input_path, output_path):
    """
    处理单个Excel文件
    
    参数:
        input_path: 输入Excel文件路径
        output_path: 输出Excel文件路径
    
    返回:
        tuple: (原始行数, 处理后行数, value最小值, value最大值)
    """
    # 读取原始Excel文件（跳过第一行表头）
    df = pd.read_excel(input_path, header=0, names=['from_id', 'to_id', 'value'])
    
    original_count = len(df)
    
    # 将from_id和to_id转换为数值类型
    df['from_id'] = pd.to_numeric(df['from_id'], errors='coerce')
    df['to_id'] = pd.to_numeric(df['to_id'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # 去除无效数据行
    df = df.dropna(subset=['from_id', 'to_id', 'value'])
    
    # 去除 from_id == to_id 的行（不符合 from_id > to_id 的要求）
    df = df[df['from_id'] != df['to_id']]
    
    # 如果from_id < to_id，则交换两列顺序
    df = df.copy()
    mask = df['from_id'] < df['to_id']
    df.loc[mask, ['from_id', 'to_id']] = df.loc[mask, ['to_id', 'from_id']].values
    
    # 去除from_id和to_id重复的行
    filtered_df = df.drop_duplicates(subset=['from_id', 'to_id'], keep='first')
    
    # 对value进行最小-最大归一化处理（缩放到[0, 1]范围）
    min_val = filtered_df['value'].min()
    max_val = filtered_df['value'].max()
    filtered_df = filtered_df.copy()
    filtered_df['normalized_value'] = (filtered_df['value'] - min_val) / (max_val - min_val)
    
    # 保存结果到新的Excel文件
    filtered_df.to_excel(output_path, index=False)
    
    return original_count, len(filtered_df), min_val, max_val
