from dafny import Dafny
from llm.llm import LLM
from invariants import insert_invariants
from modes import Modes, VALID_MODES, precheck
import argparse
import os
import tqdm


def vprint(verbose, *args, **kwargs):
    if verbose:
        print(*args, **kwargs)


def read_dafny(dafny, path):
    verified, msg = dafny.verify(path)
    with open(path, "r") as f:
        prg = f.read()
    return verified, prg


def add_invariants(dafny, llm, mode, prg):
    if mode.is_singlestep:
        inv_prg = llm.rewrite_with_invariants(prg, mode=mode)
    else:
        inv = llm.produce_invariants(prg)
        inv_prg = insert_invariants(dafny, llm, prg, inv, mode=mode)
    return inv_prg


def save_dafny(dafny, filename, content):
    if not os.path.exists("llm-generated"):
        os.mkdir("llm-generated")
    output = f"llm-generated/{filename}"
    with open(output, "w") as f:
        f.write(content)
    return dafny.verify(output)


def process_file(dafny, llm, mode, path, verbose=False):
    verified, prg = read_dafny(dafny, path)
    if verified:
        vprint(verbose, "Verified without modification")
        return None
    precheck(prg, mode)
    vprint(verbose, "---------------")
    vprint(verbose, "Invoking LLM")
    inv_prg = add_invariants(dafny, llm, mode, prg)
    vprint(verbose, "---------------")
    verified_inv, msg_inv = save_dafny(dafny, path[path.rfind("/"):], inv_prg)
    if verified_inv:
        vprint(verbose, "Verified with modification")
    else:
        vprint(verbose, "Verification failed:")
        vprint(verbose, msg_inv)
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=False)
    parser.add_argument("-d", "--directory", help="Process all files in a directory", action="store_true")
    parser.add_argument("-m", "--insert-invariants-mode", help=f"insert invariants using: {', '.join(VALID_MODES)}", default="llm")
    parser.add_argument("--dafny-path", help="dafny path", default="dafny")
    parser.add_argument("--grazie-token", help="Grazie JWT token", default=os.getenv("GRAZIE_JWT_TOKEN"))
    parser.add_argument("--llm-profile", help="llm profile", default="gpt-4-1106-preview")
    args = parser.parse_args()
    mode = Modes(args.insert_invariants_mode)
    if args.input is None:
        args.input = input("Input file: ")
    dafny = Dafny(args.dafny_path)
    llm = LLM(args.grazie_token, args.llm_profile)

    if os.path.isdir(args.input):
        if args.directory is not True:
            print("Expected a file, got a directory. Pass `--directory` to process all files")
            return
        verified_before = 0
        verified_after = 0
        failed_to_verify = 0

        files = os.listdir(args.input)
        for file in tqdm.tqdm(files):
            filepath = os.path.join(args.input, file)
            if os.path.isdir(filepath):
                # print(f"Subdirectories not supported, skipping {file}, TODO")
                continue
            # print(f"Processing {file}")
            result = process_file(dafny, llm, mode, filepath, verbose=False)
            if result is None:
                verified_before += 1
            elif result is False:
                failed_to_verify += 1
            else:
                verified_after += 1
        total_processed = verified_before + verified_after + failed_to_verify
        total_verified = verified_before + verified_after
        print("Results:")
        print(f"Total files: {total_processed}")
        if total_processed == 0:
            return
        print(f"Total verified: {total_verified} ({round(total_verified * 100 / total_processed)}%)")
        print(f"Verified without modification: {verified_before} ({verified_before * 100 / total_processed}%)")
        print(f"Verified with modification: {verified_after} ({verified_after * 100 / total_processed}%)")
        print(f"Failed to verify: {failed_to_verify} ({failed_to_verify * 100 / total_processed}%)")
    else:
        process_file(dafny, llm, mode, args.input, verbose=True)


if __name__ == '__main__':
    main()
