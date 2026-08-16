import random
import subprocess
import os
import json
from datetime import datetime, timedelta

FILE_PATH = 'random_text_changes.txt'
STATE_PATH = 'committed_days.json'  # tracks which days we've already committed, so re-runs don't duplicate


def run_git(args, env=None):
    subprocess.run(['git'] + list(args), check=True, env=env)


def load_committed_days():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, 'r') as f:
            return set(json.load(f))
    return set()


def save_committed_days(days):
    with open(STATE_PATH, 'w') as f:
        json.dump(sorted(days), f)


def write_random_comments(num_comments):
    with open(FILE_PATH, 'a') as f:
        for _ in range(num_comments):
            comment = f"# Comment on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f.write(comment)


def automate_commits():
    start_date = datetime(datetime.now().year, 1, 1)
    days_in_year = 365
    days_to_commit = int(0.73 * days_in_year)

    random_days = sorted(random.sample(range(days_in_year), days_to_commit))
    today = datetime.now()

    already_committed = load_committed_days()

    run_git(['config', 'user.name', 'Sonu0Sharma'])
    run_git(['config', 'user.email', 'sonusharmaxiisci@gmail.com'])

    made_any_commit = False

    for day_offset in random_days:
        commit_date = start_date + timedelta(days=day_offset)
        if commit_date > today:
            break

        date_key = commit_date.strftime('%Y-%m-%d')
        if date_key in already_committed:
            continue  # already committed for this day, skip so we don't pile up duplicates

        num_comments = random.randint(1, 7)
        write_random_comments(num_comments)

        run_git(['add', FILE_PATH])

        # Confirm something is actually staged before committing
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'])
        if result.returncode == 0:
            continue

        date_str = commit_date.strftime('%Y-%m-%dT12:00:00')
        commit_env = os.environ.copy()
        commit_env['GIT_AUTHOR_DATE'] = date_str
        commit_env['GIT_COMMITTER_DATE'] = date_str

        commit_message = f"Automated update for {date_key} ({num_comments} changes)"
        run_git(['commit', '-m', commit_message], env=commit_env)

        already_committed.add(date_key)
        made_any_commit = True

    if made_any_commit:
        save_committed_days(already_committed)
        run_git(['add', STATE_PATH])
        run_git(['commit', '-m', 'Update committed-days tracking file'])
        run_git(['push'])
    else:
        print("No new days to commit today.")


if __name__ == "__main__":
    automate_commits()
