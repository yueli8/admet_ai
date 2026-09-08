import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 读取CSV文件（自动检测分隔符）
df = pd.read_csv("predict.csv", sep=None, engine='python')

print("="*80)
print("口服吸收主要指标分析报告")
print("="*80)
print(f"\n成功读取文件！")
print(f"共 {len(df)} 个分子，{len(df.columns)} 个指标")
print(f"\n文件的前5列名：")
for i, col in enumerate(df.columns[:5], 1):
    print(f"  列{i}: {col}")

# 定义口服吸收的关键指标（可能的列名变体）
absorption_metrics = {
    '人肠道吸收': ['人肠道吸收', 'HIA_Hou', 'HIA'],
    'Caco-2渗透性': ['Caco-2渗透性', 'Caco2_Wang', 'Caco2'],
    'P-gp底物': ['P-gp底物', 'Pgp_Broccatelli', 'Pgp'],
    '口服生物利用度': ['口服生物利用度', 'Bioavailability_Ma', 'Bioavailability'],
    'PAMPA渗透性': ['PAMPA渗透性', 'PAMPA_NCATS', 'PAMPA'],
    '水溶性(logS)': ['水溶性(logS)', 'Solubility_AqSolDB', 'Solubility'],
    '亲脂性(logP)': ['亲脂性(logP)', 'Lipophilicity_AstraZeneca', 'Lipophilicity'],
    '血浆蛋白结合率': ['血浆蛋白结合率', 'PPBR_AZ', 'PPBR']
}

# 找到实际的列名
actual_columns = {}
key_columns = []

# 首先确定分子名称和SMILES列
name_col = None
smiles_col = None

for col in df.columns:
    col_lower = col.lower()
    if 'name' in col_lower or '名称' in col:
        name_col = col
        key_columns.append(col)
    elif 'smiles' in col_lower or 'SMILES结构式' in col:
        smiles_col = col
        key_columns.append(col)

print(f"\n分子名称列: {name_col}")
print(f"SMILES列: {smiles_col}")

# 查找吸收相关指标
print("\n" + "="*80)
print("口服吸收关键指标:")
print("="*80)

for chinese_name, possible_names in absorption_metrics.items():
    found = False
    for possible in possible_names:
        if possible in df.columns:
            actual_columns[chinese_name] = possible
            key_columns.append(possible)
            print(f"✓ {chinese_name}: {possible}")
            found = True
            break
    if not found:
        print(f"✗ 未找到: {chinese_name}")

# 提取数据
key_columns = list(dict.fromkeys(key_columns))  # 去重
absorption_df = df[key_columns].copy()

print(f"\n提取的列: {key_columns}")
print(f"数据形状: {absorption_df.shape}")

# 分析每个分子的口服吸收性能并计算综合评分
print("\n" + "="*80)
print("口服吸收性能评估:")
print("="*80)

# 创建评估结果列表
evaluation_results = []

for idx, row in absorption_df.iterrows():
    name = row[name_col] if name_col else f"分子{idx+1}"
    smiles = row[smiles_col] if smiles_col else "N/A"
    
    print(f"\n{'='*60}")
    print(f"【{name}】")
    print(f"{'='*60}")
    
    # 初始化评估结果
    eval_dict = {
        '分子名称': name,
        'SMILES结构式': smiles,
        '人肠道吸收': None,
        'HIA评估': None,
        'Caco-2渗透性': None,
        'Caco-2评估': None,
        'P-gp底物': None,
        'P-gp评估': None,
        '口服生物利用度': None,
        '生物利用度评估': None,
        'PAMPA渗透性': None,
        '水溶性(logS)': None,
        '水溶性评估': None,
        '亲脂性(logP)': None,
        '亲脂性评估': None,
        '综合评分': None,
        '评级': None,
        '星级': None
    }
    
    # 1. 人肠道吸收 (HIA)
    hia_col = actual_columns.get('人肠道吸收')
    if hia_col and hia_col in row and pd.notna(row[hia_col]):
        try:
            hia = float(row[hia_col])
            eval_dict['人肠道吸收'] = f"{hia:.4f}"
            if hia >= 0.7:
                status = "✅ 优秀"
                desc = "药物被肠道吸收的概率高"
            elif hia >= 0.5:
                status = "⚠️ 中等"
                desc = "药物被肠道吸收的概率中等"
            else:
                status = "❌ 较差"
                desc = "药物被肠道吸收的概率低"
            eval_dict['HIA评估'] = status
            print(f"\n📊 人肠道吸收 (HIA): {hia:.4f} {status}")
            print(f"   {desc}")
        except:
            print(f"\n📊 人肠道吸收: 数据格式错误")
    
    # 2. Caco-2渗透性
    caco2_col = actual_columns.get('Caco-2渗透性')
    if caco2_col and caco2_col in row and pd.notna(row[caco2_col]):
        try:
            caco2 = float(row[caco2_col])
            eval_dict['Caco-2渗透性'] = f"{caco2:.4f}"
            if caco2 > -5.15:
                status = "✅ 高渗透性"
                desc = "药物容易穿过肠上皮细胞"
            elif caco2 > -6.0:
                status = "⚠️ 中等渗透性"
                desc = "药物穿过肠上皮细胞的能力中等"
            else:
                status = "❌ 低渗透性"
                desc = "药物难以穿过肠上皮细胞"
            eval_dict['Caco-2评估'] = status
            print(f"\n📊 Caco-2细胞渗透性: {caco2:.4f} {status}")
            print(f"   {desc}")
        except:
            print(f"\n📊 Caco-2渗透性: 数据格式错误")
    
    # 3. P-gp底物
    pgp_col = actual_columns.get('P-gp底物')
    if pgp_col and pgp_col in row and pd.notna(row[pgp_col]):
        try:
            pgp = float(row[pgp_col])
            eval_dict['P-gp底物'] = f"{pgp:.4f}"
            if pgp < 0.3:
                status = "✅ 非P-gp底物"
                desc = "不会被外排泵排出，有利于吸收"
            elif pgp < 0.5:
                status = "⚠️ 可能是弱P-gp底物"
                desc = "可能被外排泵部分排出"
            else:
                status = "❌ P-gp底物"
                desc = "容易被外排泵排出，影响吸收"
            eval_dict['P-gp评估'] = status
            print(f"\n📊 P-gp底物: {pgp:.4f} {status}")
            print(f"   {desc}")
        except:
            print(f"\n📊 P-gp底物: 数据格式错误")
    
    # 4. 口服生物利用度
    bioavail_col = actual_columns.get('口服生物利用度')
    if bioavail_col and bioavail_col in row and pd.notna(row[bioavail_col]):
        try:
            bioavail = float(row[bioavail_col])
            eval_dict['口服生物利用度'] = f"{bioavail:.4f}"
            if bioavail >= 0.7:
                status = "✅ 高生物利用度"
                desc = "药物进入体循环的比例高"
            elif bioavail >= 0.5:
                status = "⚠️ 中等生物利用度"
                desc = "药物进入体循环的比例中等"
            else:
                status = "❌ 低生物利用度"
                desc = "药物进入体循环的比例低"
            eval_dict['生物利用度评估'] = status
            print(f"\n📊 口服生物利用度: {bioavail:.4f} {status}")
            print(f"   {desc}")
        except:
            print(f"\n📊 口服生物利用度: 数据格式错误")
    
    # 5. PAMPA渗透性
    pampa_col = actual_columns.get('PAMPA渗透性')
    if pampa_col and pampa_col in row and pd.notna(row[pampa_col]):
        try:
            pampa = float(row[pampa_col])
            eval_dict['PAMPA渗透性'] = f"{pampa:.4f}"
            print(f"\n📊 PAMPA渗透性: {pampa:.4f}")
            print(f"   被动扩散渗透性指标")
        except:
            print(f"\n📊 PAMPA渗透性: 数据格式错误")
    
    # 6. 水溶性
    solubility_col = actual_columns.get('水溶性(logS)')
    if solubility_col and solubility_col in row and pd.notna(row[solubility_col]):
        try:
            solubility = float(row[solubility_col])
            eval_dict['水溶性(logS)'] = f"{solubility:.4f}"
            if solubility > -4:
                status = "✅ 可溶性好"
                desc = "在水中溶解性好，有利于吸收"
            elif solubility > -6:
                status = "⚠️ 中等溶解性"
                desc = "在水中溶解性中等"
            else:
                status = "❌ 难溶"
                desc = "在水中难溶，可能影响吸收"
            eval_dict['水溶性评估'] = status
            print(f"\n📊 水溶性 (logS): {solubility:.4f} {status}")
            print(f"   {desc}")
        except:
            print(f"\n📊 水溶性: 数据格式错误")
    
    # 7. 亲脂性
    lipo_col = actual_columns.get('亲脂性(logP)')
    if lipo_col and lipo_col in row and pd.notna(row[lipo_col]):
        try:
            lipo = float(row[lipo_col])
            eval_dict['亲脂性(logP)'] = f"{lipo:.4f}"
            if 1 <= lipo <= 3:
                status = "✅ 适中"
                desc = "亲脂性适中，有利于跨膜吸收"
            elif lipo < 1:
                status = "⚠️ 偏亲水"
                desc = "偏亲水，可能影响跨膜吸收"
            else:
                status = "⚠️ 偏亲脂"
                desc = "偏亲脂，可能影响水溶性"
            eval_dict['亲脂性评估'] = status
            print(f"\n📊 亲脂性 (logP): {lipo:.4f} {status}")
            print(f"   {desc}")
        except:
            print(f"\n📊 亲脂性: 数据格式错误")
    
    # 计算综合评分
    score = 0
    weight_sum = 0
    
    # HIA评分（权重30%）
    if hia_col and hia_col in row and pd.notna(row[hia_col]):
        try:
            score += float(row[hia_col]) * 0.3
            weight_sum += 0.3
        except:
            pass
    
    # Caco-2评分（权重20%）
    if caco2_col and caco2_col in row and pd.notna(row[caco2_col]):
        try:
            caco2_val = float(row[caco2_col])
            caco2_score = 1 / (1 + np.exp(-(caco2_val + 5.5)))
            score += caco2_score * 0.2
            weight_sum += 0.2
        except:
            pass
    
    # P-gp评分（权重20%，非底物为佳）
    if pgp_col and pgp_col in row and pd.notna(row[pgp_col]):
        try:
            score += (1 - float(row[pgp_col])) * 0.2
            weight_sum += 0.2
        except:
            pass
    
    # 生物利用度评分（权重30%）
    if bioavail_col and bioavail_col in row and pd.notna(row[bioavail_col]):
        try:
            score += float(row[bioavail_col]) * 0.3
            weight_sum += 0.3
        except:
            pass
    
    if weight_sum > 0:
        final_score = score / weight_sum
        eval_dict['综合评分'] = f"{final_score:.4f}"
        
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
        
        eval_dict['评级'] = rating
        eval_dict['星级'] = stars
        
        print(f"\n📈 综合评分: {final_score:.4f} {stars} ({rating})")
    
    evaluation_results.append(eval_dict)

# 创建最终的合并表格
final_df = pd.DataFrame(evaluation_results)

# 保存合并后的表格
output_file = "口服吸收完整分析结果.csv"
final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n{'='*80}")
print(f"✅ 完整分析结果已保存到: {output_file}")
print(f"{'='*80}")

# 显示合并后的表格
print(f"\n合并后的完整表格:")
print(f"{'='*80}")
print(final_df.to_string(index=False))

print("\n分析完成！")
