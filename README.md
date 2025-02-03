# Review Buddy

## Description

Review Buddy is a command-line Python application that, given a GitHub username, fetches all code and QA reviews 
performed by the specified user between now and a specified date.

## Installation

1. Clone the repository
2. Install the required packages by running `pip install -r requirements.txt`
3. Run the application by running `python review_buddy.py -u <username> --starting-at="Month Day Year"`
4. (optional) For convenience, add an alias to the above in your `.zshrc`:
   `alias review-buddy="python /path/to/review_buddy.py -u <username>"`
5. Generate a GitHub personal access token to store in your Keychain. Copy it or save it somewhere temporarily.
   - as of February 2025, this can be done in your [GitHub Settings > Developer Settings > Personal Access Tokens > 
     Tokens (classic)](https://github.com/settings/tokens)  

## Usage

The default usage of this application checks for a GitHub personal access token in the system's Keychain, prompts for 
one if not found, and then fetches all reviews performed by the specified user by checking GitHub's published Events
pertaining to the user. You can force an update of the stored access token with the `--edit-access-token` flag.

Provide an optional `--starting-at` date to specify the earliest date to fetch reviews from. GitHub's events API only returns about
a month's worth of events, but this can be useful for filtering out older reviews. **Defaults to the previous Monday**.

### Examples

```bash
$ python review_buddy.py -u samueljackson-wf
$ python review_buddy.py -u samueljackson-wf --starting-at="Jan 1 2025"
```