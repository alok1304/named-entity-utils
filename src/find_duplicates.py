import hashlib
import json
import argparse
from pathlib import Path
from collections import defaultdict
from licensedcode.tokenize import index_tokenizer_with_stopwords
from licensedcode.frontmatter import load_frontmatter


def hash_tokens(t):
    h = hashlib.sha256()
    for tk in t:
        h.update(str(tk).encode("utf-8"))
    return h.hexdigest()


def find_similar_rules(paths, out_path):
    hashes = defaultdict(list)
    r_files = []

    for path in paths:
        p = Path(path)
        if p.is_file() and p.suffix.upper() == ".RULE":
            r_files.append(p)
        elif p.is_dir():
            r_files.extend(p.rglob("*.RULE"))
        else:
            print(f"Skipping invalid path: {p}")

    if not r_files:
        print("No .RULE files found in given paths.")
        return

    print(f"Scanning and tokenizing {len(r_files)} .RULE files...")

    for f in r_files:
        try:
            content,metadata = load_frontmatter(f)
            license_exp=metadata.get("license_expression")
            if not license_exp or metadata.get("is_deprecated"):
                license_exp=""  
            t = index_tokenizer_with_stopwords(license_exp+content)
            if not t or metadata.get("is_deprecated"):
                continue
            t_hash = hash_tokens(t)
            hashes[t_hash].append(str(f.resolve()))
        except Exception as e:
            print(f"Could not process {f}: {e}")

    sim_groups = []
    for _, files in hashes.items():
        if len(files) > 1:
            sim_groups.append(sorted(files))

    if not sim_groups:
        print("🎉 No similar .RULE files were found.")
        return

    if out_path:
        # Convert full paths to just filenames for the JSON output
        json_groups = [[Path(fp).name for fp in group] for group in sim_groups]
        results = {"duplicates rules": json_groups}
        try:
            with open(out_path, 'w', encoding='utf-8') as jf:
                json.dump(results, jf, indent=2)
            print(f"Scan complete. Results saved to {out_path}")
        except IOError as e:
            print(f"Error writing to file {out_path}: {e}")
    else:
        print("Scan complete. Reporting similar rules...")
        print("-" * 40)
        for group in sim_groups:
            print("Found a set of functionally equivalent rules:")
            for fname in group:
                print(f"  - {fname}")
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Finds functionally similar .RULE files based on tokenized content."
    )
    parser.add_argument(
        'paths',
        nargs='+',
        help="One or more files or directories to scan."
    )
    parser.add_argument(
        '--output', '-o',
        metavar='FILE',
        help="Save the results to a JSON file instead of printing to console."
    )
    args = parser.parse_args()

    find_similar_rules(args.paths, args.output)