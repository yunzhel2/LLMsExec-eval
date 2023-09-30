import os.path
from pathlib import Path
from collections import Counter
import json
import datasets
import pandas as pd
from datasets import load_from_disk,load_dataset

from api_comm import APICommunication, ExtendedUnittest

data_file_path = r'C:\Users\36914\PycharmProjects\cs410\codeforces_data'

def execute_code(language, source_code, unittests):
    api = APICommunication()
    response = api.execute_code(
        language=language,
        source_code=source_code,
        unittests=unittests
    )
    print(response)

    response_datas = response[0]
    exec_outcomes = []
    results = []
    if isinstance(response_datas, list):
        for response_data in response_datas:
            exec_outcomes.append(response_data['exec_outcome'])
            results.append(response_data['result'])
    else:
        exec_outcomes.append('UNKNOWN_ERROR')
        results.append('')

    return exec_outcomes, results

Example = {"lang":"Java 11","source_code":"import java.lang.*;\nimport java.util.*;\n\npublic class Cost{\n    public static void main(String[] args){\n        Scanner sc=new Scanner(System.in);\n        int n=sc.nextInt();\n        int[] arr=new int[n];\n        int negCount=0;\n        int negMax=-100;\n        int posCount=0;\n        for(int i=0; i<n; i++){\n            arr[i]=sc.nextInt();\n            if(arr[i]>0) posCount++;\n            if(arr[i]<0){\n                negCount++;\n                if(arr[i]>=negMax){\n                    negMax=arr[i];\n                }\n            }\n        }\n        for(int i=0; i<n; i++){\n            if(arr.length==1){\n                System.out.print(arr[0]);\n                return;\n            }\n            if(negCount%2==1 && arr[i]==negMax){\n                negMax=-101;\n                continue;\n            }\n            else{\n                if(arr[i]!=0){\n                    System.out.print(arr[i]+\" \");\n                }\n                else{\n                    if(posCount==0 && (negCount==0 || negCount==1)){\n                        System.out.print(0);\n                        return;\n                    }\n                }\n            }\n        }\n    }\n}","tags":["greedy"],"lang_cluster":"Java","src_uid":"b11644953bdd1b92eb1b18c339a268a1","code_uid":"e6092062d04df2f5d889af6cd8cd4ace","difficulty":1400,"exec_outcome":"PASSED",
           "task_id":"b11644953bdd1b92eb1b18c339a268a1",
           'hidden_unit_tests':'[ { "input": "5  1 2 -3 3 3 ", "time": [ "0"],"mem": ["4"],"output": ["3 1 2 3 "]},]'
    }


def add_exec_outcome(example):
    language = example['lang']
    source_code = example['source_code']
    # unittest = example['task_uid']]
    try:
        hidden_unit_tests = eval(example['hidden_unit_tests'])
    except:
        print(example['hidden_unit_tests'])
    unittests = []
    for hidden_unit_test in hidden_unit_tests:
        unittests.append(
            ExtendedUnittest(
                input=hidden_unit_test['input'],
                output=hidden_unit_test['output']
            ).json()
        )

    exec_outcomes, results = execute_code(language, source_code, unittests)
    print(exec_outcomes)
    print(results)

    if all(exec_outcome == 'PASSED' for exec_outcome in exec_outcomes):
        example['all_passed'] = 1
    else:
        example['all_passed'] = 0

    return example


def main():
    # load_path = Path(__file__).parent.parent / Path('data') / Path('lang_data')
    load_path = os.path.join(data_file_path,'lyz_1000.jsonl')
    unittest_path = os.path.join(data_file_path, 'testcases_0822.jsonl')
    # unittests = pd.read_json(unittest_path, orient='records', lines=True)
    save_path = os.path.join(data_file_path,'lyz_1000_valid.jsonl')
    # data = pd.read_json(load_path,lines=True)
    datasets = load_dataset('json', split=None, data_files=str(load_path))
    dataset = datasets['train']
    dataset.cleanup_cache_files()
    print(dataset)
    # dataset['hidden_unit_tests'] =  unittests[dataset['src_uid']]
    dataset = dataset.map(add_exec_outcome)
    print(dataset)

    lang_counts = Counter(dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_cluster_counts = Counter(dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    dataset.save_to_disk(save_path)


if __name__ == '__main__':
    main()

    # add_exec_outcome(Example)
    # python scripts/execute_data.py