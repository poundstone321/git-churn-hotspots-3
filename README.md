# git-churn-hotspots

Hey. I wrote this because I was digging through a gnarly embedded codebase and wanted a quick way to see which files we were constantly hacking on—our true architectural pain points.

It runs `git log` under the hood, parses commit history, and spits out a ranked list of files based on change frequency (churn). Fuelled by cold brew and mechanical keyboard clatter.

## Usage

```bash
python churn.py /path/to/repo -n 10
```

Options:
- `-n`, `--top`: Number of top files to display (default: 10)
- `--since`: Limit history (e.g., '1 year ago', '6 months ago')
