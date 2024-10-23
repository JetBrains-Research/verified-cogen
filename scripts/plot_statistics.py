# %%
with open('log_tries/logs3.txt', 'r') as file:
    # Read the file and split the contents into lines
    lines = file.readlines()

# set_errors = {
#
# }

dict_erros = {
    "Not supported:" : 0,
    "The precondition of" : 0,
    "Type error:" : 0,
    "Invalid program:" : 0,
    "Postcondition of" : 0,
    "Loop invariant might not be preserved." : 0,
    "Loop invariant might not hold on entry." : 0,
    "Assert might fail." : 0,
}

explanations = {
    "Not supported:" : "Not supported \n(list comprehensions or \ndouble inequalities ... )",
    "The precondition of" : "precondition doesn't hold",
    "Type error:" : "Type error (invalid arguments, \ncannot infer types, \nalready defined variables ... )",
    "Invalid program:" : "Invalid program (invariants in random places ...)",
    "Postcondition of" : "postcondition doesn't hold",
    "Loop invariant might not be preserved." : "Loop invariant might not be preserved",
    "Loop invariant might not hold on entry." : "Loop invariant might not hold on entry",
    "Assert might fail." : "Assert might fail",
}

dict_erros_numbered = {}

for (key, value) in dict_erros.items():
    for j in range(1, 11):
        dict_erros_numbered[(key, j)] = 0

print(dict_erros_numbered)

# The 'lines' variable will now be a list of lines from the file
idx_line = 0
for line in lines:
    if "Verification failed:" in line:
        idx_line += 1
    if "verified with" in line:
        idx_line = 0
    if idx_line == 11:
        idx_line = 1
    for (key, value) in dict_erros.items():
        if key in line:
            dict_erros[key] += 1
            dict_erros_numbered[(key, idx_line)] += 1


print(dict_erros)
print(dict_erros_numbered)

for (key, value) in dict_erros_numbered.items():
    print(key, value)


import matplotlib.pyplot as plt

error_data = {}
for (error_type, try_number), occurrences in dict_erros_numbered.items():

    error_type = explanations[error_type]

    if error_type not in error_data:
        error_data[error_type] = {"tries": [], "occurrences": []}
    error_data[error_type]["tries"].append(try_number)
    error_data[error_type]["occurrences"].append(occurrences)

# Step 2: Plot the data
plt.figure(figsize=(10, 11))

for error_type, data in error_data.items():
    plt.plot(data["tries"], data["occurrences"], marker='o', label=error_type)

# Step 3: Customize the plot
plt.xlabel('Try')

tries_range = range(1, 11)  # Assuming the "tries" are from 1 to 5
plt.xticks(tries_range)

plt.ylabel('Number of Occurrences')
plt.title('Error Occurrences in Benchmark by Try')
plt.legend(title="Error Types", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()