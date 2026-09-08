import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 读取CSV文件（逗号分隔）
df = pd.read_csv("all_predictions.csv", sep=',')

print("="*80)
print("口服吸收主要指标分析报告")
print("="*80)
print(f"\n成功读取文件！")
print(f"共 {len(df)} 个分子，{len(df.columns)} 个指标")

# 定义口服吸收的关键指标（英文列名 -> 中英文显示名）
absorption_metrics = {
    'HIA_Hou': 'HIA_Hou\n人肠道吸收',
    'Caco2_Wang': 'Caco2_Wang\nCaco-2渗透性',
    'Pgp_Broccatelli': 'Pgp_Broccatelli\nP-gp底物',
    'Bioavailability_Ma': 'Bioavailability_Ma\n口服生物利用度',
    'PAMPA_NCATS': 'PAMPA_NCATS\nPAMPA渗透性',
    'Solubility_AqSolDB': 'Solubility_AqSolDB\n水溶性(logS)',
    'Lipophilicity_AstraZeneca': 'Lipophilicity_AstraZeneca\n亲脂性(logP)',
    'PPBR_AZ': 'PPBR_AZ\n血浆蛋白结合率'
}

# 提取口服吸收相关指标
print("\n" + "="*80)
print("口服吸收关键指标:")
print("="*80)

# 创建包含关键指标的数据框
key_columns = ['Name', 'SMILES']
available_metrics = {}

for col in absorption_metrics.keys():
    if col in df.columns:
        key_columns.append(col)
        available_metrics[col] = absorption_metrics[col]
        print(f"✓ {absorption_metrics[col].replace(chr(10), ' ')}: {col}")
    else:
        print(f"✗ 未找到: {col}")

# 提取数据
absorption_df = df[key_columns].copy()

# 分析每个分子的口服吸收性能并计算综合评分
print("\n" + "="*80)
print("口服吸收性能评估:")
print("="*80)

# 创建评估结果列表
evaluation_results = []

for idx, row in absorption_df.iterrows():
    name = row['Name']
    smiles = row['SMILES']
    
    print(f"\n{'='*60}")
    print(f"【{name}】")
    print(f"{'='*60}")
    
    # 初始化评估结果
    eval_dict = {
        'Name': name,
        'SMILES': smiles,
        'HIA_Hou\n人肠道吸收': None,
        'HIA_Status\nHIA评估': None,
        'Caco2_Wang\nCaco-2渗透性': None,
        'Caco2_Status\nCaco-2评估': None,
        'Pgp_Broccatelli\nP-gp底物': None,
        'Pgp_Status\nP-gp评估': None,
        'Bioavailability_Ma\n口服生物利用度': None,
        'Bioavailability_Status\n生物利用度评估': None,
        'PAMPA_NCATS\nPAMPA渗透性': None,
        'Solubility_AqSolDB\n水溶性(logS)': None,
        'Solubility_Status\n水溶性评估': None,
        'Lipophilicity_AstraZeneca\n亲脂性(logP)': None,
        'Lipophilicity_Status\n亲脂性评估': None,
        'Comprehensive_Score\n综合评分': None,
        'Rating\n评级': None,
        'Stars\n星级': None
    }
    
    # 1. 人肠道吸收 (HIA)
    if 'HIA_Hou' in row and pd.notna(row['HIA_Hou']):
        hia = row['HIA_Hou']
        eval_dict['HIA_Hou\n人肠道吸收'] = f"{hia:.4f}"
        if hia >= 0.7:
            status = "✅ 优秀"
            desc = "药物被肠道吸收的概率高"
        elif hia >= 0.5:
            status = "⚠️ 中等"
            desc = "药物被肠道吸收的概率中等"
        else:
            status = "❌ 较差"
            desc = "药物被肠道吸收的概率低"
        eval_dict['HIA_Status\nHIA评估'] = status
        print(f"\n📊 人肠道吸收 (HIA): {hia:.4f} {status}")
        print(f"   {desc}")
    
    # 2. Caco-2渗透性
    if 'Caco2_Wang' in row and pd.notna(row['Caco2_Wang']):
        caco2 = row['Caco2_Wang']
        eval_dict['Caco2_Wang\nCaco-2渗透性'] = f"{caco2:.4f}"
        if caco2 > -5.15:
            status = "✅ 高渗透性"
            desc = "药物容易穿过肠上皮细胞"
        elif caco2 > -6.0:
            status = "⚠️ 中等渗透性"
            desc = "药物穿过肠上皮细胞的能力中等"
        else:
            status = "❌ 低渗透性"
            desc = "药物难以穿过肠上皮细胞"
        eval_dict['Caco2_Status\nCaco-2评估'] = status
        print(f"\n📊 Caco-2细胞渗透性: {caco2:.4f} {status}")
        print(f"   {desc}")
    
    # 3. P-gp底物
    if 'Pgp_Broccatelli' in row and pd.notna(row['Pgp_Broccatelli']):
        pgp = row['Pgp_Broccatelli']
        eval_dict['Pgp_Broccatelli\nP-gp底物'] = f"{pgp:.4f}"
        if pgp < 0.3:
            status = "✅ 非P-gp底物"
            desc = "不会被外排泵排出，有利于吸收"
        elif pgp < 0.5:
            status = "⚠️ 可能是弱P-gp底物"
            desc = "可能被外排泵部分排出"
        else:
            status = "❌ P-gp底物"
            desc = "容易被外排泵排出，影响吸收"
        eval_dict['Pgp_Status\nP-gp评估'] = status
        print(f"\n📊 P-gp底物: {pgp:.4f} {status}")
        print(f"   {desc}")
    
    # 4. 口服生物利用度
    if 'Bioavailability_Ma' in row and pd.notna(row['Bioavailability_Ma']):
        bioavail = row['Bioavailability_Ma']
        eval_dict['Bioavailability_Ma\n口服生物利用度'] = f"{bioavail:.4f}"
        if bioavail >= 0.7:
            status = "✅ 高生物利用度"
            desc = "药物进入体循环的比例高"
        elif bioavail >= 0.5:
            status = "⚠️ 中等生物利用度"
            desc = "药物进入体循环的比例中等"
        else:
            status = "❌ 低生物利用度"
            desc = "药物进入体循环的比例低"
        eval_dict['Bioavailability_Status\n生物利用度评估'] = status
        print(f"\n📊 口服生物利用度: {bioavail:.4f} {status}")
        print(f"   {desc}")
    
    # 5. PAMPA渗透性
    if 'PAMPA_NCATS' in row and pd.notna(row['PAMPA_NCATS']):
        pampa = row['PAMPA_NCATS']
        eval_dict['PAMPA_NCATS\nPAMPA渗透性'] = f"{pampa:.4f}"
        print(f"\n📊 PAMPA渗透性: {pampa:.4f}")
        print(f"   被动扩散渗透性指标")
    
    # 6. 水溶性
    if 'Solubility_AqSolDB' in row and pd.notna(row['Solubility_AqSolDB']):
        solubility = row['Solubility_AqSolDB']
        eval_dict['Solubility_AqSolDB\n水溶性(logS)'] = f"{solubility:.4f}"
        if solubility > -4:
            status = "✅ 可溶性好"
            desc = "在水中溶解性好，有利于吸收"
        elif solubility > -6:
            status = "⚠️ 中等溶解性"
            desc = "在水中溶解性中等"
        else:
            status = "❌ 难溶"
            desc = "在水中难溶，可能影响吸收"
        eval_dict['Solubility_Status\n水溶性评估'] = status
        print(f"\n📊 水溶性 (logS): {solubility:.4f} {status}")
        print(f"   {desc}")
    
    # 7. 亲脂性
    if 'Lipophilicity_AstraZeneca' in row and pd.notna(row['Lipophilicity_AstraZeneca']):
        lipo = row['Lipophilicity_AstraZeneca']
        eval_dict['Lipophilicity_AstraZeneca\n亲脂性(logP)'] = f"{lipo:.4f}"
        if 1 <= lipo <= 3:
            status = "✅ 适中"
            desc = "亲脂性适中，有利于跨膜吸收"
        elif lipo < 1:
            status = "⚠️ 偏亲水"
            desc = "偏亲水，可能影响跨膜吸收"
        else:
            status = "⚠️ 偏亲脂"
            desc = "偏亲脂，可能影响水溶性"
        eval_dict['Lipophilicity_Status\n亲脂性评估'] = status
        print(f"\n📊 亲脂性 (logP): {lipo:.4f} {status}")
        print(f"   {desc}")
    
    # 计算综合评分
    score = 0
    count = 0
    
    # HIA评分（权重30%）
    if 'HIA_Hou' in row and pd.notna(row['HIA_Hou']):
        score += row['HIA_Hou'] * 0.3
        count += 1
    
    # Caco-2评分（权重20%）
    if 'Caco2_Wang' in row and pd.notna(row['Caco2_Wang']):
        caco2_score = 1 / (1 + np.exp(-(row['Caco2_Wang'] + 5.5)))
        score += caco2_score * 0.2
        count += 1
    
    # P-gp评分（权重20%，非底物为佳）
    if 'Pgp_Broccatelli' in row and pd.notna(row['Pgp_Broccatelli']):
        score += (1 - row['Pgp_Broccatelli']) * 0.2
        count += 1
    
    # 生物利用度评分（权重30%）
    if 'Bioavailability_Ma' in row and pd.notna(row['Bioavailability_Ma']):
        score += row['Bioavailability_Ma'] * 0.3
        count += 1
    
    if count > 0:
        final_score = score / (0.3 + 0.2 + 0.2 + 0.3)
        eval_dict['Comprehensive_Score\n综合评分'] = f"{final_score:.4f}"
        
        if final_score >= 0.8:
            rating = "优秀"
            stars = "★★★★★"
        elif final_score >= 0.7:
            rating = "良好"
            stars = "★★★★"
        elif final_score >= 0.6:
            rating = "中等"
            stars = "★★★"
        elif final_score >= 0.5:
            rating = "较差"
            stars = "★★"
        else:
            rating = "很差"
            stars = "★"
        
        eval_dict['Rating\n评级'] = rating
        eval_dict['Stars\n星级'] = stars
        
        print(f"\n📈 综合评分: {final_score:.4f} {stars} ({rating})")
    
    evaluation_results.append(eval_dict)

# 创建最终的合并表格
final_df = pd.DataFrame(evaluation_results)

# 保存合并后的表格
output_file = "oral_absorption_complete_analysis.csv"
final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n{'='*80}")
print(f"✅ 完整分析结果已保存到: {output_file}")
print(f"{'='*80}")

# 显示合并后的表格
print(f"\n合并后的完整表格:")
print(f"{'='*80}")
print(final_df.to_string(index=False))

# 创建简化版表格（只包含关键信息）
simple_df = final_df[[
    'Name', 
    'HIA_Hou\n人肠道吸收',
    'HIA_Status\nHIA评估',
    'Caco2_Wang\nCaco-2渗透性',
    'Caco2_Status\nCaco-2评估',
    'Pgp_Broccatelli\nP-gp底物',
    'Pgp_Status\nP-gp评估',
    'Bioavailability_Ma\n口服生物利用度',
    'Bioavailability_Status\n生物利用度评估',
    'Comprehensive_Score\n综合评分',
    'Rating\n评级',
    'Stars\n星级'
]].copy()

simple_output = "oral_absorption_summary.csv"
simple_df.to_csv(simple_output, index=False, encoding='utf-8-sig')
print(f"\n✅ 简化版表格已保存到: {simple_output}")

print(f"\n简化版表格:")
print(f"{'='*80}")
print(simple_df.to_string(index=False))

print("\n" + "="*80)
print("指标说明:")
print("="*80)
print("""
1. **HIA_Hou (人肠道吸收)**: 
   - 预测药物被人体肠道吸收的概率
   - >0.7: 吸收良好；0.5-0.7: 中等；<0.5: 较差

2. **Caco2_Wang (Caco-2细胞渗透性)**:
   - 反映药物穿过肠上皮细胞的能力
   - >-5.15: 高渗透性；-5.15~-6.0: 中等；<-6.0: 低渗透性

3. **Pgp_Broccatelli (P-gp底物)**:
   - P-糖蛋白外排泵的底物
   - <0.3: 非底物（好）；0.3-0.5: 弱底物；>0.5: 底物（差）

4. **Bioavailability_Ma (口服生物利用度)**:
   - 药物进入体循环的比例
   - >0.7: 高；0.5-0.7: 中等；<0.5: 低

5. **综合评分**:
   - 加权计算：HIA(30%) + Caco-2(20%) + P-gp(20%) + 生物利用度(30%)
   - >0.8: 优秀；0.7-0.8: 良好；0.6-0.7: 中等；0.5-0.6: 较差；<0.5: 很差
""")

print("\n分析完成！")
