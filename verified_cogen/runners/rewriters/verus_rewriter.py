from typing import Optional

from verified_cogen.args import LLMConfig
from verified_cogen.runners.rewriters import Rewriter
from verified_cogen.tools import extract_code_from_llm_output

FIX_SPEC_TYPES_PROMPT = """
Let's fix array access integer types in specification/proof code according to Verus's best practices:

For proof/spec code (functions marked with spec fn or proof fn):
- When accessing arrays, use int or nat for indices rather than fixed-width types
- Ensure array indices have proper type conversions if needed

For example, change:
spec fn get_array_element(arr: Seq<u32>, i: u32) -> u32 { arr[i] }
To:
spec fn get_array_element(arr: Seq<u32>, i: u32) -> u32 { arr[i as int] }

Please fix only the array access integer types in proof/spec code while preserving the core functionality and verification properties.
Return only the fixed code without explanations.

REMEMBER TO ONLY DO THIS IN PROOF/ASSERTS AND SPEC/PROOF FUNCTIONS. DO NOT CHANGE EXECUTABLE CODE.

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
        if error is None:
            return prg, ""
        assert self.llm_with_idx is not None

        llm_config, idx = self.llm_with_idx
        llm = llm_config.build(idx)

        llm.add_user_prompt(FIX_SPEC_TYPES_PROMPT.replace("{program}", prg).replace("{error}", error))
        result = extract_code_from_llm_output(llm.make_request())

        prompt = f"After applying fixes to array access integer types in spec/proof code (converting fixed-width types to int/nat for array indices), the updated code is:\n{result}"
        return result, prompt
