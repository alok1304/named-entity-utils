import argparse
from remove_named_entities import process_path, remove_named_entities

def main():
    parser = argparse.ArgumentParser(
        description="Remove named entities (PERSON, ORG, GPE) from text files."
    )
    parser.add_argument("path", help="Path to file or folder")
    parser.add_argument(
        "-o", "--output",
        help="Output folder (default: overwrite in-place)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "-l", "--license-expression",
        help="Only process files with this license expression",
        required=True   
    )

    args = parser.parse_args()

    if args.dry_run:
        with open(args.path, "r", encoding="utf-8") as f:
            text = f.read()
        print(remove_named_entities(text))
    else:
        process_path(args.path, output=args.output, license_expression=args.license_expression)


if __name__ == "__main__":
    main()
