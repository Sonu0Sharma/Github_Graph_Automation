import random
from datetime import datetime, timedelta
import os

# Define the path for the text file in the same repository
file_path = 'random_text_changes.txt'
start_date = datetime(datetime.now().year, 1, 1)  # Start from Jan 1 of this year
days_in_year = 365

# Calculate 73% of the year in days
days_to_commit = int(0.73 * days_in_year)

# Generate random days for commits
random_days = sorted(random.sample(range(days_in_year), days_to_commit))

# Function to write a random comment in the file multiple times for a given day
def write_random_comments(num_comments):
    with open(file_path, 'a') as f:
        for _ in range(num_comments):
            comment = f"# Comment on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f.write(comment)

# Main function to simulate committing changes
def automate_commits():
    today = datetime.now()
    for day_offset in random_days:
        commit_date = start_date + timedelta(days=day_offset)
        if commit_date > today:
            break
        
        # Set the date for simulated commit
        os.environ['GIT_COMMITTER_DATE'] = commit_date.strftime('%Y-%m-%dT12:00:00')
        os.environ['GIT_AUTHOR_DATE'] = commit_date.strftime('%Y-%m-%dT12:00:00')
        
        # Generate a random number of comments (1-7) for this day
        num_comments = random.randint(1, 7)
        write_random_comments(num_comments)

if __name__ == "__main__":
    automate_commits()
