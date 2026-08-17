import csv
import re

def convert_to_csv_auto_detect(input_file='input.txt', output_file='molecules.csv'):
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()
    
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # 按行处理
        for line in content.split('\n'):
            if line.strip():
                # 使用正则表达式分割，支持Tab或多个空格
                parts = re.split(r'\t+|\s{2,}', line.strip())
                if len(parts) >= 2:
                    # 清理可能的额外空格
                    parts = [p.strip() for p in parts]
                    writer.writerow(parts[:2])  # 只取前两列
    
    print(f"转换完成！输出文件：{output_file}")

# 执行转换
if __name__ == "__main__":
    convert_to_csv_auto_detect('input.txt', 'molecules.csv')
