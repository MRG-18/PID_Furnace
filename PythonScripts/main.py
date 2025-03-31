#!/usr/bin/env python3
"""
This script generates fake commits in a Git repository from June 1, 2024 until today.
It creates roughly 3 to 5 commits per week (averaging around 4) with randomized times,
so that your GitHub contributions graph will show activity throughout that period.
    
WARNING: Manipulating commit dates to inflate contribution history may be considered unethical
or misleading. Use this script responsibly and only in contexts where it is acceptable.
"""

import datetime
import random
import subprocess
import os

def generate_commit_dates(start_date, end_date):
    """
    Generate a sorted list of datetime objects representing when commits should be made.
    For each week between start_date and end_date, randomly choose between 3 and 5 commits.
    """
    commit_dates = []
    current = start_date
    # Loop week by week
    while current < end_date.date():
        # Randomize the number of commits this week (3 to 5)
        commits_this_week = random.randint(3, 5)
        for _ in range(commits_this_week):
            # Random day in the week (0 to 6 days after the week's start)
            day_offset = random.randint(0, 6)
            commit_day = current + datetime.timedelta(days=day_offset)
            # Do not exceed the end_date
            if commit_day > end_date.date():
                commit_day = end_date.date()
            # Pick a random time during typical working hours (9am to 8pm)
            hour = random.randint(9, 20)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_datetime = datetime.datetime.combine(commit_day, datetime.time(hour, minute, second))
            commit_dates.append(commit_datetime)
        # Advance one week
        current += datetime.timedelta(days=7)
    commit_dates.sort()
    return commit_dates

def make_commit(commit_date):
    """
    Append a line to a dummy file and commit it with the commit date set via environment variables.
    """
    commit_date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")
    filename = "dummy.txt"
    
    # Append a line so that the file changes and the commit is not completely empty.
    with open(filename, "a") as f:
        f.write(f"Fake commit on {commit_date_str}\n")
    
    # Stage the changes
    subprocess.run(["git", "add", filename], check=True)
    
    # Set environment variables for commit dates
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date_str
    env["GIT_COMMITTER_DATE"] = commit_date_str
    
    commit_message = f"Fake commit for {commit_date_str}"
    # Using --allow-empty as a fallback (if, for example, there's nothing to commit)
    subprocess.run(["git", "commit", "--allow-empty", "-m", commit_message], env=env, check=True)
    print(f"Committed: {commit_message}")

def main():
    # Check if we're in a Git repository
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: This script must be run inside a Git repository.")
        return

    # Set the period: starting June 1, 2024 until the current moment
    start_date = datetime.date(2024, 6, 1)
    end_date = datetime.datetime.now()

    commit_dates = generate_commit_dates(start_date, end_date)
    print(f"Generating {len(commit_dates)} fake commits from {start_date} to {end_date.date()}...")

    # Create the commits one by one
    for commit_date in commit_dates:
        make_commit(commit_date)

    # Finally, push your changes to GitHub.
    # Note: Ensure that your branch is set up correctly and that you're okay with rewriting history if needed.
    subprocess.run(["git", "push"], check=True)
    print("All fake commits have been pushed.")

if __name__ == "__main__":
    main()
