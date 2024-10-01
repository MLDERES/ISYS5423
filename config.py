from dotenv import load_dotenv
import os
import base64
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

key_vault_url = "https://story-feedback-kv.vault.azure.net/"

def get_secret(secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    return client.get_secret(secret_name).value

load_dotenv()

#USER_STORY_REVIEW_PAT = os.getenv("FA_TOKEN")
USER_STORY_REVIEW_PAT = get_secret("FA-TOKEN")
DEVOPS_AUTH_TOKEN = f'{base64.b64encode(f"PAT:{USER_STORY_REVIEW_PAT}".encode("utf-8")).decode("utf-8")}'
DEVOPS_ORG = "WCOB-ISYS5423"
API_VERSION = "7.1-preview.2"
PRIMARY_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {DEVOPS_AUTH_TOKEN}',
    }
#OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_API_KEY = get_secret("OPENAI-API-KEY")

STORY_BACKGROUND="""
You are reviewing a user story written by a business school student pursuing a degree in information systems. The student is learning about software development and user stories as part of their coursework.
Please evaluate the quality of the following user story based on the criteria below. If no user story is provided or if it is incomplete, kindly note that it cannot be evaluated.
User Story Quality Criteria:
- Independent: Should be self-contained, allowing it to be released without depending on other stories.
- Negotiable: Captures the essence of the user's need while leaving room for discussion, rather than being overly prescriptive or rigid like a contract.
- Valuable: Delivers tangible value to the end user or business.
- Estimable: Can be estimated for effort, allowing prioritization and planning within sprints.
- Small: Small enough to be completed in 3-4 days within a sprint.
- Testable: Includes pre-written acceptance criteria that confirm whether the story is complete and works as expected.
Evaluation:
Assess each category with one of the following: Needs Work, Good, Great. Provide feedback on how to improve it if necessary.
Overall Quality: [Needs Work / Good / Great]
- Independent: [Needs Work / Good / Great]  
  Feedback:
- Negotiable: [Needs Work / Good / Great]  
  Feedback:
- Valuable: [Needs Work / Good / Great]  
  Feedback:
- Estimable: [Needs Work / Good / Great]  
  Feedback:
- Small: [Needs Work / Good / Great]  
  Feedback:
- Testable: [Needs Work / Good / Great]  
  Feedback:
---
Acceptance Criteria Quality: [Needs Work / Good / Great]
The acceptance criteria should follow this format:
- This story will be finished when: {Expected outcome, clearly testable}
- Out of scope: {Any areas not covered by this story}
Note: The acceptance criteria must be specific, testable, and clear. If the student has left this blank or written something too vague to be tested, provide feedback on how to improve it.
---
Suggestions for Improvement:  
If applicable, suggest an alternative version of the user story that better fits the criteria.
---
Additional Notes:
- Use a positive, constructive tone to guide the student’s learning process.
- If there is no user story provided, or the submission is blank, acknowledge that it cannot be evaluated and suggest submitting a complete story for feedback.
"""