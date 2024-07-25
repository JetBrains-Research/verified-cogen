import os

import datasets
from datasets import *


def load_humaneval():
    data = load_dataset("THUDM/humaneval-x", "python")
    print(data["test"][0])
    print(data["test"][0]['declaration'] + data["test"][0]['canonical_solution'] + data["test"][0]['example_test'])
    print(data["test"][0]['prompt'])
    idx1 = data["test"][0]['declaration'].find("def")
    idx2 = data["test"][0]['declaration'].find("(")
    print(data["test"][0]['declaration'][idx1 + 4 : idx2])
    print(len(data["test"]))

    for i in range(9, len(data["test"])):
        idx1 = data["test"][i]['declaration'].find("def")
        idx2 = data["test"][i]['declaration'].find("(")
        name = data["test"][i]['declaration'][idx1 + 4 : idx2]
        directory_path = str(i) + '_' + name 
        
        os.makedirs(directory_path, exist_ok=True)
        file_pat_py = os.path.join(directory_path, name + '.' + 'py')
        content_py = data["test"][i]['declaration'] + data["test"][i]['canonical_solution'] + data["test"][i]['example_test']
        
        with open(file_pat_py, 'w') as file:
            file.write(content_py)
        
        file_pat_prompt = os.path.join(directory_path, name + '.' + 'prompt')
        content_prompt = data["test"][i]['prompt']       
        
        with open(file_pat_prompt, 'w') as file:
            file.write(content_prompt)

if __name__ == '__main__':
    load_humaneval()