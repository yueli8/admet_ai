import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from admet_ai import ADMETModel
import pandas as pd
import sys

def predict_from_csv(input_file, output_file="predictions.csv"):
    """
    从 CSV 文件读取 SMILES 并进行 ADMET 预测
    
    参数:
    input_file: 输入 CSV 文件路径（需要包含 SMILES 列）
    output_file: 输出 CSV 文件路径
    """
    
    # 初始化模型
    print("正在加载 ADMET-AI 模型...")
    model = ADMETModel()
    
    # 读取输入文件
    try:
        df_input = pd.read_csv(input_file)
        print(f"成功读取输入文件: {input_file}")
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：读取文件时出现问题 - {e}")
        sys.exit(1)
    
    # 检查列名（不区分大小写）
    smiles_column = None
    for col in df_input.columns:
        if col.upper() == 'SMILES':
            smiles_column = col
            break
    
    # 如果没找到 SMILES 列，使用第一列
    if smiles_column is None:
        smiles_column = df_input.columns[0]
        print(f"警告：未找到 'SMILES' 列，使用第一列 '{smiles_column}' 作为 SMILES")
    
    # 提取 SMILES 列表
    smiles_list = df_input[smiles_column].dropna().tolist()
    print(f"共读取到 {len(smiles_list)} 个有效分子")
    
    if len(smiles_list) == 0:
        print("错误：没有找到有效的 SMILES 数据")
        sys.exit(1)
    
    # 进行预测
    print("正在进行 ADMET 预测...")
    try:
        results = model.predict(smiles_list)
    except Exception as e:
        print(f"错误：预测过程中出现问题 - {e}")
        sys.exit(1)
    
    # 转换为 DataFrame
    df_results = pd.DataFrame(results)
    
    # 确保 SMILES 列在最前面
    if 'SMILES' in df_results.columns:
        cols = ['SMILES'] + [col for col in df_results.columns if col != 'SMILES']
        df_results = df_results[cols]
    
    # 保存结果
    df_results.to_csv(output_file, index=False)
    print(f"预测完成！结果已保存到: {output_file}")
    
    # 显示统计信息
    print(f"\n预测结果统计：")
    print(f"- 总分子数: {len(df_results)}")
    print(f"- 预测属性数: {len(df_results.columns) - 1}")
    
    return df_results

if __name__ == "__main__":
    # 使用示例
    input_file = "molecules.csv"  # 修改为你的输入文件路径
    output_file = "predictions.csv"  # 修改为你的输出文件路径
    
    # 可以通过命令行参数指定输入输出文件
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    # 运行预测
    df_results = predict_from_csv(input_file, output_file)
    
    # 显示前几行结果
    print("\n预测结果预览（前5行）：")
    print(df_results.head())
