from src.commands.command import Command
from src.constants import REVIEW_TYPE_QA_REVIEW, REVIEW_TYPE_CODE_REVIEW

from datetime import datetime, timezone

from github import Github, PullRequest

class FetchReviews(Command):
    def __init__(self, user: str, gh: Github, starting_at: datetime):
        self.user = user
        self.gh = gh
        self.starting_at = starting_at

    @staticmethod
    def output_pr_review(
        pr_num: int,
        pr_author: str,
        pr_url: str,
        type: str,
        date: datetime,
    ):
        print(f'{pr_num}, {pr_author}, {pr_url}, {type}, {date}')

    def check_event(self, event, pr_key, comment_key, created_at):
        if pr_key not in event.payload:
            return
        if comment_key not in event.payload:
            return

        pr = event.payload[pr_key]
        author = pr['user']['login']

        if self.user == author:
            return

        number = pr['number']
        url = pr['url']

        comment = event.payload[comment_key]

        is_qa = comment['body'] and 'QA +1' in comment['body']
        self.output_pr_review(
            number,
            author,
            url,
            REVIEW_TYPE_QA_REVIEW if is_qa else REVIEW_TYPE_CODE_REVIEW,
            created_at)

    def apply(self):
        user = self.gh.get_user(self.user)
        events = user.get_events()

        for event in events:
            created_at = event.created_at.replace(tzinfo=timezone.utc)
            if created_at < self.starting_at:
                break

            if 'PullRequestReviewEvent' == event.type:
                self.check_event(event, 'pull_request', 'review', created_at)
            elif 'PullRequestReviewCommentEvent' == event.type:
                self.check_event(event, 'pull_request', 'comment', created_at)
            elif 'IssueCommentEvent' == event.type:
                self.check_event(event, 'issue', 'comment', created_at)
