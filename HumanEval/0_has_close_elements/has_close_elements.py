from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
   for idx, elem in enumerate(numbers):
       for idx2, elem2 in enumerate(numbers):
           if idx != idx2:
               distance = abs(elem - elem2)
               if distance < threshold:
                   return True


   return False

def check(has_close_elements):
    assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
    assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True

check(has_close_elements)
print(has_close_elements([1.0, 2.0, 3.0], 0.5))