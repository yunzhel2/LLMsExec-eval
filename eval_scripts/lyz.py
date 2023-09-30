import os.path
from collections import Counter

import datasets
from datasets import load_dataset
from api_comm import APICommunication, ExtendedUnittest


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


def add_exec_outcome(example):
    language = example['lang']
    source_code = example['source_code']
    hidden_unit_tests = eval(example['hidden_unit_tests'])

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

    base_path = r'C:\Users\36914\PycharmProjects\cs410\codeforces_data'
    dataset = datasets.Dataset.from_json(os.path.join(base_path,'api_test_submission_java.jsonl')).select(list(range(10000)))

    # dataset = load_dataset('NTU-NLP-sg/xCodeEval', 'code_translation',)
    # print(dataset)
    dataset.cleanup_cache_files()
    dataset = dataset.filter(lambda example: example['lang_cluster'] == 'Javascript')
    print(dataset)

    lang_counts = Counter(dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_cluster_counts = Counter(dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    dataset = dataset.map(add_exec_outcome)
    print(dataset)

    dataset.to_json('lyz.jsonl', lines=True)


if __name__ == '__main__':
    main()
