from utils import extract_core_content,jinahtml2string
# born date, height, weight, nationality, club, position, salary, market value, 
from duckduckgo_search import DDGS
from utils import openai_wrapper
from PromptsAndClasses.DynamicDataFormat import create_pydantic_class,DataExtractPrompt
import concurrent.futures
from functools import partial

# 应该去对相关的网页进行解析，最后去相关的效果进行说明
# jina.ai
def extract_info_from_webpage(search_query,position_query):
    results = DDGS().text(search_query)
    if results and 'href' in results[0]:
        url = results[0]['href']
        result_text = jinahtml2string(url)
        extracted_info = {}
        
        # use the index key to find the corrsponding result for htis list
        if result_text:
            for position in position_query:
                # Look for the position in the result text
                index = result_text.lower().find(position.lower())
                if index != -1:
                    # Determine boundaries for surrounding text
                    start_index = max(0, index - 500)
                    end_index = min(len(result_text), index + 500 + len(position))
                    
                    # Extract surrounding text
                    surrounding_text = result_text[start_index:end_index]
                    extracted_info[position] = surrounding_text
        # Convert the extracted_info dictionary to a single string
        aggregated_text = " ".join([f"{key}: {value}" for key, value in extracted_info.items()])
        
        # Update result_text with the aggregated string
        result_text = aggregated_text
        print(f"length of the result_text is {len(result_text)}")
        return result_text
    else:
        print("No valid URL found in the search results.")
        return None

def process_row(row, column_names, response_format):
    key_column = row[0]
    search_query = f"{key_column} football player"
    print(search_query)
    web_result = extract_info_from_webpage(search_query, position_query=column_names)

    web_result = web_result[:3000]
    openai_result = openai_wrapper(system_messages=DataExtractPrompt,
                input_messages=web_result,
                response_format=response_format)
    print(openai_result)
    
    return openai_result.dict()


def process_dataframe_parallel(df, max_workers=4):
    print('processing the data')
    column_names = df.columns.tolist()
    column_names.pop(0)
    fields_dict = {col: 'str' for col in column_names}
    response_format = create_pydantic_class('Response', fields_dict)

    process_row_partial = partial(process_row, column_names=column_names, response_format=response_format)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_row_partial, [row for _, row in df.iterrows()]))

    for index, result in enumerate(results):
        for key, value in result.items():
            df.at[index, key] = value

    return df