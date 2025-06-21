import argparse
from code_reviewer.pipeline import run_pipeline

def main() -> None:
    parser = argparse.ArgumentParser(description="Run AI code review on a repo.")
    parser.add_argument("--repo", required=True, help="Path to the git repository")
    args = parser.parse_args()

    run_pipeline(args.repo)

if __name__ == "__main__":
    main()
