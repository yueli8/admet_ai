import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from admet_ai import ADMETModel
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 初始化模型
print("正在加载ADMET-AI模型...")
model = ADMETModel()
print("模型加载完成！\n")

# 读取CSV文件（逗号分隔）
input_file = "molecules.csv"  # 修改为你的文件路径
df_input = pd.read_csv(input_file, sep=',')

print(f"输入文件内容:")
print(df_input)
print(f"\n总共 {len(df_input)} 个分子\n")

# 提取SMILES和名称
smiles_list = df_input['SMILES'].tolist()
names_list = df_input['Name'].tolist()

print(f"SMILES列表 ({len(smiles_list)}个):")
for i, (name, smiles) in enumerate(zip(names_list, smiles_list), 1):
    print(f"  {i}. {name}: {smiles}")

# 开始预测
print("\n开始预测所有分子...")
all_results = []

for i, (name, smiles) in enumerate(zip(names_list, smiles_list), 1):
    print(f"\n{'='*60}")
    print(f"预测第 {i}/{len(smiles_list)} 个分子: {name}")
    print(f"SMILES: {smiles}")
    
    try:
        # 预测单个分子
        result = model.predict(smiles)
        
        # 处理返回结果
        if isinstance(result, list):
            if len(result) > 0:
                result = result[0]
            else:
                result = {}
        
        # 添加原始信息到结果中
        result['SMILES'] = smiles
        result['Name'] = name
        
        all_results.append(result)
        print(f"✅ {name} 预测完成")
        
        # 显示关键结果
        if '分子量' in result:
            print(f"   分子量: {result['分子量']:.4f}")
        if 'LogP' in result:
            print(f"   LogP: {result['LogP']:.4f}")
        if 'AMES毒性' in result:
            print(f"   AMES毒性: {result['AMES毒性']:.4f}")
            
    except Exception as e:
        print(f"❌ {name} 预测失败: {e}")
        # 创建一个空结果，保留原始信息
        all_results.append({'SMILES': smiles, 'Name': name, 'Error': str(e)})

# 创建最终结果DataFrame
if all_results:
    df_results = pd.DataFrame(all_results)
    
    # 重新排列列顺序，把Name和SMILES放在前面
    cols = ['Name', 'SMILES'] + [col for col in df_results.columns if col not in ['Name', 'SMILES']]
    df_results = df_results[cols]
    
    # 保存结果
    output_file = "all_predictions.csv"
    df_results.to_csv(output_file, index=False, sep=',')
    
    print(f"\n{'='*60}")
    print(f"✅ 所有预测完成！")
    print(f"结果已保存到: {output_file}")
    print(f"共处理 {len(df_results)} 个分子")
    print(f"结果包含 {len(df_results.columns)} 个属性列")
    
    # 显示完整结果表格
    print(f"\n完整预测结果:")
    print(df_results)
    
    # 显示关键性质对比
    print(f"\n{'='*60}")
    print("关键性质对比:")
    print(f"{'='*60}")
    key_properties = ['Name', '分子量', 'LogP', 'QED', 'AMES毒性', '口服吸收', '心脏毒性', '生物利用度']
    available_props = [prop for prop in key_properties if prop in df_results.columns]
    if available_props:
        print(df_results[available_props].to_string(index=False))
    
else:
    print("没有成功预测任何分子")

print(f"\n程序执行完成！")
