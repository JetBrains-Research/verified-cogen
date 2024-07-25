# Description of the Dataset and work done
Here i tried to produce Dafny, Viper and Nagini analogs for Python functions from [HumalEval](https://huggingface.co/datasets/openai/openai_humaneval) dataset. I asked GPT4 model to produce Dafny code **file.dfy** from provided task prompt **file.prompt** and python code **file.py**. Then I asked GPT4 to generate Viper code **file.vpr** and nagini **file.nagini** code from given dafny code. I modified provided outputs so that invariants become verifiable and meaningful. 

Due to limitations of target languages (like inability to work with strings, etc) and the fact that some programs are trivial, different counterparts were produced for the following programs: 
* Dafny - 0, 1, 5, 6, 7, 9, 10, 11, 12, 13, 14
* Viper - 0, 5, 9, 13
* Nagini - 0, 5, 9, 13

### Prompt for generating Dafny code: 

    Generate pre/postconditions with Dafny code for this prompt and python code: 
 
    from typing import List


    def separate_paren_groups(paren_string: str) -> List[str]:
        """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
        separate those group into separate strings and return the list of those.
        Separate groups are balanced (each open brace is properly closed) and not nested within each other
        Ignore any spaces in the input string.
        >>> separate_paren_groups('( ) (( )) (( )( ))')
        ['()', '(())', '(()())']
        """
        
    from typing import List


    def separate_paren_groups(paren_string: str) -> List[str]:
        result = []
        current_string = []
        current_depth = 0

        for c in paren_string:
            if c == '(':
                current_depth += 1
                current_string.append(c)
            elif c == ')':
                current_depth -= 1
                current_string.append(c)

                if current_depth == 0:
                    result.append(''.join(current_string))
                    current_string.clear()

        return result

    def check(separate_paren_groups):
        assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']
    check(separate_paren_groups)
    print(separate_paren_groups('( ) (( )) (( )( ))')) 


### General hints (ideas): 
* It seems like Viper and Nagini do not support strings 
* Nullable types (see [9_rolling_max](9_rolling_max)) can be replaced with self-written `Optional` in Dafny, `Ref` in Viper and library `Optional` in Nagini
* `Seq` is analog for `List` in Dafny and Viper
* Nagini requires preconditions and invariants, like `Invariant(Acc(list_pred(numbers)))` (where `numbers` - list). `Acc(list_pred(numbers))` expresses the ability to get values of list elements and to modify list
* Concerning Dafny and Viper: `method` - regular function; `function` is used in a predicate (there can be no loops in `function`, however, recursion can be used)
* It seems like GPT4 has better knowledge of Dafny, compared to Viper and Nagini



### Additional: 
* [Dafny Reference Manual](https://dafny.org/dafny/DafnyRef/DafnyRef#sec-function-declaration)
* [Viper Tutorial](https://viper.ethz.ch/tutorial/)
* [Nagini](https://github.com/marcoeilers/nagini)
* We found ~750 problems, written in Dafny [here](https://github.com/sun-wendy/DafnyBench)