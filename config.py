from dotenv import load_dotenv
import os
import base64

load_dotenv()
USER_STORY_REVIEW_PAT = os.getenv("FA_TOKEN")
DEVOPS_AUTH_TOKEN = f'{base64.b64encode(f"PAT:{USER_STORY_REVIEW_PAT}".encode("utf-8")).decode("utf-8")}'
DEVOPS_ORG = "WCOB-ISYS5423"
API_VERSION = "7.2-preview.2"
PRIMARY_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {DEVOPS_AUTH_TOKEN}',
    }
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

STORY_BACKGROUND="""
The user receiving the feedback is a student in a business school pursuing a degree in information systems. 
The student is taking a course on software development and is learning about user stories.

I want to assess this quality of this user story for these criteria:
Independent: Should be self-contained in a way that allows to be released without depending on one another.
Negotiable: Only capture the essence of user's need, leaving room for conversation. User story should not be written like contract.
Valuable: Delivers value to end user.
Estimable: User stories have to able to be estimated so it can be properly prioritized and fit into sprints.
Small: A user story is a small chunk of work that allows it to be completed in about 3 to 4 days.
Testable: A user story has to be confirmed via pre-written acceptance criteria.

Please assess the quality of this user story (using a 'needs work', 'good' or 'great') and then provide feedback on how to improve it if required.

Use a template like this:
Overall quality: [needs work, good, great]
Independent: a few words on how to improve this or not
Negotiable: a few words on how to improve this or not
Valuable: a few words on how to improve this or not
Estimable: a few words on how to improve this or not
Small: a few words on how to improve this or not
Testable: a few words on how to improve this or not

Acceptance Criteria: [needs work, good, great]
a few words on how to improve this or not

If it would be valuable, offer an alternative user story that would be better.

"""