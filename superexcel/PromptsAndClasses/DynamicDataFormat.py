from pydantic import BaseModel,Field
def create_pydantic_class(class_name: str, fields: dict):
    """
    动态创建一个Pydantic数据类。
    
    :param class_name: 类名
    :param fields: 一个字典，其中key是字段名，value是字段类型
    :return: Pydantic数据类
    """
    namespace = {"__annotations__": fields}
    return type(class_name, (BaseModel,), namespace)


DataExtractPrompt = """
You are an information extraction assistant. Your task is to extract specific information from the provided text.

Information extraction requirements and considerations:
- Please extract the info that we need
- Ensure the extracted information is accurate and disregard unrelated information.
- The output should be structured for further use.
- if you don't find it just return : 'not found'

3. Example:
Input: Lionel Messi was born on June 24, 1987, in Rosario, Argentina. He plays for Paris Saint-Germain as a forward. His height is 170 cm and he weighs 72 kg. Currently, his market value is approximately €80 million and his annual salary is €30 million.
Output:
{
    "birth-date": "June 24, 1987",
    "height": "170 cm",
    "weight": "72 kg",
    "nationality": "Argentina",
    "club": "Paris Saint-Germain",
    "position": "forward",
    "salary": "€30 million",
    "market-value": "€80 million"
}
"""

if __name__ == "__main__":
    # 示例使用
    results = {
        "height": str,
        "weight": str,
    }
    # this is what I need...
    results = create_pydantic_class("results", results)

    # 创建示例数据
    sample_data = {
        "height": "180 cm",
        "weight": "75 kg"
    }

    # 使用生成的 Pydantic 类进行实例化
    results_instance = results(**sample_data)

    # 打印实例以验证结果
    print(results_instance)