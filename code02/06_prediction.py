import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 读取CSV文件（逗号分隔）
df = pd.read_csv("predictions567.csv", sep=',')

# 定义英文列名到中文列名的映射
column_name_mapping = {
    'Name': '分子名称',
    'SMILES': 'SMILES结构式',
    'molecular_weight': '分子量',
    'logP': '脂水分配系数(logP)',
    'hydrogen_bond_acceptors': '氢键受体数',
    'hydrogen_bond_donors': '氢键供体数',
    'Lipinski': 'Lipinski规则',
    'QED': '药物相似性(QED)',
    'stereo_centers': '立体中心数',
    'tpsa': '拓扑极性表面积(TPSA)',
    'AMES': 'AMES致突变性',
    'BBB_Martins': '血脑屏障渗透性',
    'Bioavailability_Ma': '口服生物利用度',
    'CYP1A2_Veith': 'CYP1A2抑制剂',
    'CYP2C19_Veith': 'CYP2C19抑制剂',
    'CYP2C9_Substrate_CarbonMangels': 'CYP2C9底物',
    'CYP2C9_Veith': 'CYP2C9抑制剂',
    'CYP2D6_Substrate_CarbonMangels': 'CYP2D6底物',
    'CYP2D6_Veith': 'CYP2D6抑制剂',
    'CYP3A4_Substrate_CarbonMangels': 'CYP3A4底物',
    'CYP3A4_Veith': 'CYP3A4抑制剂',
    'Carcinogens_Lagunin': '致癌性',
    'ClinTox': '临床毒性',
    'DILI': '药物性肝损伤',
    'HIA_Hou': '人肠道吸收',
    'NR-AR-LBD': '雄激素受体配体结合域',
    'NR-AR': '雄激素受体',
    'NR-AhR': '芳香烃受体',
    'NR-Aromatase': '芳香化酶',
    'NR-ER-LBD': '雌激素受体配体结合域',
    'NR-ER': '雌激素受体',
    'NR-PPAR-gamma': '过氧化物酶体增殖物激活受体γ',
    'PAMPA_NCATS': 'PAMPA渗透性',
    'Pgp_Broccatelli': 'P-gp底物',
    'SR-ARE': '抗氧化反应元件',
    'SR-ATAD5': 'ATAD5应激反应',
    'SR-HSE': '热休克反应元件',
    'SR-MMP': '线粒体膜电位',
    'SR-p53': 'p53应激反应',
    'Skin_Reaction': '皮肤反应',
    'hERG': 'hERG心脏毒性',
    'Caco2_Wang': 'Caco-2渗透性',
    'Clearance_Hepatocyte_AZ': '肝细胞清除率',
    'Clearance_Microsome_AZ': '微粒体清除率',
    'Half_Life_Obach': '半衰期',
    'HydrationFreeEnergy_FreeSolv': '水合自由能',
    'LD50_Zhu': '急性毒性(LD50)',
    'Lipophilicity_AstraZeneca': '亲脂性(logP)',
    'PPBR_AZ': '血浆蛋白结合率',
    'Solubility_AqSolDB': '水溶性(logS)',
    'VDss_Lombardo': '稳态分布容积',
    'molecular_weight_drugbank_approved_percentile': '分子量(DrugBank已批准药物百分位)',
    'logP_drugbank_approved_percentile': '脂水分配系数(DrugBank已批准药物百分位)',
    'hydrogen_bond_acceptors_drugbank_approved_percentile': '氢键受体数(DrugBank已批准药物百分位)',
    'hydrogen_bond_donors_drugbank_approved_percentile': '氢键供体数(DrugBank已批准药物百分位)',
    'Lipinski_drugbank_approved_percentile': 'Lipinski规则(DrugBank已批准药物百分位)',
    'QED_drugbank_approved_percentile': '药物相似性(DrugBank已批准药物百分位)',
    'stereo_centers_drugbank_approved_percentile': '立体中心数(DrugBank已批准药物百分位)',
    'tpsa_drugbank_approved_percentile': '拓扑极性表面积(DrugBank已批准药物百分位)',
    'AMES_drugbank_approved_percentile': 'AMES致突变性(DrugBank已批准药物百分位)',
    'BBB_Martins_drugbank_approved_percentile': '血脑屏障渗透性(DrugBank已批准药物百分位)',
    'Bioavailability_Ma_drugbank_approved_percentile': '口服生物利用度(DrugBank已批准药物百分位)',
    'CYP1A2_Veith_drugbank_approved_percentile': 'CYP1A2抑制剂(DrugBank已批准药物百分位)',
    'CYP2C19_Veith_drugbank_approved_percentile': 'CYP2C19抑制剂(DrugBank已批准药物百分位)',
    'CYP2C9_Substrate_CarbonMangels_drugbank_approved_percentile': 'CYP2C9底物(DrugBank已批准药物百分位)',
    'CYP2C9_Veith_drugbank_approved_percentile': 'CYP2C9抑制剂(DrugBank已批准药物百分位)',
    'CYP2D6_Substrate_CarbonMangels_drugbank_approved_percentile': 'CYP2D6底物(DrugBank已批准药物百分位)',
    'CYP2D6_Veith_drugbank_approved_percentile': 'CYP2D6抑制剂(DrugBank已批准药物百分位)',
    'CYP3A4_Substrate_CarbonMangels_drugbank_approved_percentile': 'CYP3A4底物(DrugBank已批准药物百分位)',
    'CYP3A4_Veith_drugbank_approved_percentile': 'CYP3A4抑制剂(DrugBank已批准药物百分位)',
    'Carcinogens_Lagunin_drugbank_approved_percentile': '致癌性(DrugBank已批准药物百分位)',
    'ClinTox_drugbank_approved_percentile': '临床毒性(DrugBank已批准药物百分位)',
    'DILI_drugbank_approved_percentile': '药物性肝损伤(DrugBank已批准药物百分位)',
    'HIA_Hou_drugbank_approved_percentile': '人肠道吸收(DrugBank已批准药物百分位)',
    'NR-AR-LBD_drugbank_approved_percentile': '雄激素受体配体结合域(DrugBank已批准药物百分位)',
    'NR-AR_drugbank_approved_percentile': '雄激素受体(DrugBank已批准药物百分位)',
    'NR-AhR_drugbank_approved_percentile': '芳香烃受体(DrugBank已批准药物百分位)',
    'NR-Aromatase_drugbank_approved_percentile': '芳香化酶(DrugBank已批准药物百分位)',
    'NR-ER-LBD_drugbank_approved_percentile': '雌激素受体配体结合域(DrugBank已批准药物百分位)',
    'NR-ER_drugbank_approved_percentile': '雌激素受体(DrugBank已批准药物百分位)',
    'NR-PPAR-gamma_drugbank_approved_percentile': 'PPARγ(DrugBank已批准药物百分位)',
    'PAMPA_NCATS_drugbank_approved_percentile': 'PAMPA渗透性(DrugBank已批准药物百分位)',
    'Pgp_Broccatelli_drugbank_approved_percentile': 'P-gp底物(DrugBank已批准药物百分位)',
    'SR-ARE_drugbank_approved_percentile': '抗氧化反应元件(DrugBank已批准药物百分位)',
    'SR-ATAD5_drugbank_approved_percentile': 'ATAD5应激反应(DrugBank已批准药物百分位)',
    'SR-HSE_drugbank_approved_percentile': '热休克反应元件(DrugBank已批准药物百分位)',
    'SR-MMP_drugbank_approved_percentile': '线粒体膜电位(DrugBank已批准药物百分位)',
    'SR-p53_drugbank_approved_percentile': 'p53应激反应(DrugBank已批准药物百分位)',
    'Skin_Reaction_drugbank_approved_percentile': '皮肤反应(DrugBank已批准药物百分位)',
    'hERG_drugbank_approved_percentile': 'hERG心脏毒性(DrugBank已批准药物百分位)',
    'Caco2_Wang_drugbank_approved_percentile': 'Caco-2渗透性(DrugBank已批准药物百分位)',
    'Clearance_Hepatocyte_AZ_drugbank_approved_percentile': '肝细胞清除率(DrugBank已批准药物百分位)',
    'Clearance_Microsome_AZ_drugbank_approved_percentile': '微粒体清除率(DrugBank已批准药物百分位)',
    'Half_Life_Obach_drugbank_approved_percentile': '半衰期(DrugBank已批准药物百分位)',
    'HydrationFreeEnergy_FreeSolv_drugbank_approved_percentile': '水合自由能(DrugBank已批准药物百分位)',
    'LD50_Zhu_drugbank_approved_percentile': '急性毒性LD50(DrugBank已批准药物百分位)',
    'Lipophilicity_AstraZeneca_drugbank_approved_percentile': '亲脂性logP(DrugBank已批准药物百分位)',
    'PPBR_AZ_drugbank_approved_percentile': '血浆蛋白结合率(DrugBank已批准药物百分位)',
    'Solubility_AqSolDB_drugbank_approved_percentile': '水溶性logS(DrugBank已批准药物百分位)',
    'VDss_Lombardo_drugbank_approved_percentile': '稳态分布容积(DrugBank已批准药物百分位)'
}

# 重命名列
df_renamed = df.rename(columns=column_name_mapping)

# 保存重命名后的CSV文件
output_file = "predict.csv"
df_renamed.to_csv(output_file, index=False, encoding='utf-8-sig')

print("="*80)
print("列名中英文对照表")
print("="*80)
print(f"\n原始列数: {len(df.columns)}")
print(f"重命名列数: {len(df_renamed.columns)}")
print(f"\n✅ 中文版文件已保存到: {output_file}")

# 显示前几行数据
print(f"\n前5行数据预览:")
print("="*80)
print(df_renamed.head().to_string(index=False))

# 显示所有列名
print(f"\n所有列名（中文）:")
print("="*80)
for i, col in enumerate(df_renamed.columns, 1):
    print(f"{i:3d}. {col}")

print(f"\n✅ 处理完成！")
