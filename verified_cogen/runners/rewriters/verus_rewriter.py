from typing import Optional

from verified_cogen.args import LLMConfig
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.tools import extract_code_from_llm_output

FIX_INT_TYPES_PROMPT = """
The code contains mixed usage of integer types between executable code and proof/spec code. Let's fix the type usage according to Verus's best practices:

For executable code:
- Replace broad int types with specific fixed-width types like i8, i16, i32, i64, i128, isize or u8, u16, u32, u64, u128, usize
- Use appropriate size types based on the value ranges needed
- Add explicit casts where necessary with `as` operator
- Consider platform-specific types (usize/isize) when dealing with indexing or sizes

For proof/spec code (functions marked with spec fn or proof fn):
- Use int for mathematical integers and general arithmetic - this is most efficient for the SMT solver
- Use nat for non-negative integers, especially for lengths and sizes
- Replace fixed-width types with int/nat unless specific byte-level operations are needed
- Add casts to int/nat types if nesessary
- Ensure bounds are properly specified in requires/ensures clauses (with int/nat types!)

For example, change:
spec fn sum(x: u32) -> u32 {...}
To:
spec fn sum(x: int) -> int {...}

And change:
fn compute(x: int) -> int {...}
To:
fn compute(x: i32) -> i32 {...}

Please fix the integer type usage while preserving the core functionality and verification properties.
Return only the fixed code without explanations.
Program:
{program}

To help you we also include the error from the verifier. Don't rely on it too much
{error}
"""


class VerusRewriter(Rewriter):
    def __init__(self, llm: Optional[tuple[LLMConfig, int]] = None):
        super().__init__(llm)
        assert self.llm_with_idx is not None, "VerusRewriter requires LLM be set"

    def rewrite(self, prg: str, error: Optional[str] = None) -> tuple[str, str]:
        assert error is not None, "VerusRewriter requires error message"
        assert self.llm_with_idx is not None

        llm_config, idx = self.llm_with_idx
        llm = llm_config.build(idx)

        llm.add_user_prompt(FIX_INT_TYPES_PROMPT.format(program=prg, error=error))
        return extract_code_from_llm_output(llm.make_request()), ""
