#!/usr/bin/env python3
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from admet_ai import ADMETModel

print("正在加载ADMET模型（CPU模式）...")
model = ADMETModel()

test_smiles = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
print(f"测试分子: {test_smiles}")

predictions = model.predict(test_smiles)
print("\n预测结果：")
print(predictions)
