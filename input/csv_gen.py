import csv

# 人名列表
names = [
    "Pelé",
    "Diego Maradona",
    "Lionel Messi",
    "Cristiano Ronaldo",
    "Zinedine Zidane",
    "Johan Cruyff",
    "Ronaldinho",
    "Ronaldo Nazário",
    "Michel Platini",
    "Franz Beckenbauer",
    "George Best",
    "Alfredo Di Stéfano",
    "Thierry Henry",
    "Xavi Hernández",
    "Andrés Iniesta",
    "Roberto Baggio",
    "Paolo Maldini",
    "David Beckham",
    "Gerd Müller",
    "Marco van Basten"
]

# 将人名保存到CSV文件
with open('football_legends.xls', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入列名
    writer.writerow(["name"])
    # 写入人名
    for name in names:
        writer.writerow([name])
import pandas as pd
df = pd.DataFrame(names, columns=["name"])

# 保存为XLS文件
df.to_excel('football_legends.xls', index=False, encoding='utf-8')

print("XLS文件已保存为 'football_legends.xls'")


print("CSV文件已保存为 'football_legends.csv'")