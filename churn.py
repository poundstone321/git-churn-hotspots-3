import argparse
import subprocess
import sys
from collections import Counter

def run_git_log(repo_path, since=None):
    cmd = ['git', '-C', repo_path, 'log', '--name-only', '--oneline']
    if since:
        cmd.append(f'--since={since}')
        
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

def analyze_churn(log_output):
    file_counter = Counter()
    for line in log_output.splitlines():
        line = line.strip();
        if not line:
            continue
        if len(line.split(' ', 1)) == 2 and not line.startswith('/'):
            parts = line.split(' ', 1)
            if len(parts[0]) == 7 and all(c in '0123456789abcdefABCDEF' for c in parts[0]):
                continue
        if '.' in line or '/' in line:
            file_counter[line] += 1
    return file_counter

def main():
    parser = argparse.ArgumentParser(description='Identify high-churn files in a git repository.')
    parser.add_argument('repo', nargs='?', default='.', help='Path to git repository')
    parser.add_argument('-n', '--top', type=int, default=10, help='Number of top files to show')
    parser.add_argument('--since', type=str, default=None, help='Analyze commits since date (e.g. "1 year ago")')
    
    args = parser.parse_args()
    
    print(f"Scanning repo at '{args.repo}' for change frequency...")
    log_data = run_git_log(args.repo, args.since)
    churn_data = analyze_churn(log_data)
    
    print(f"\nTop {args.top} Highest-Churn Files:")
    print("-" * 40)
    for filepath, count in churn_data.most_common(args.top):
        print(f"{count:4d} changes | {filepath}")

if __name__ == '__main__':
    main()
