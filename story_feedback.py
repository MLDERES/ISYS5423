import requests
import json
import config
import openai
import tqdm
import html

# Function to fetch open user stories that haven't been "Instructor Reviewed"
def fetch_open_user_stories():
    url = f"https://dev.azure.com/"
    url += f"{config.DEVOPS_ORG}/" 
    url += f"_apis/wit/wiql"
    
    params = {"api-version":config.API_VERSION}
    
    payload = json.dumps({
          "query": """SELECT [System.Id] FROM workitems WHERE [System.WorkItemType] = 'User Story' 
          AND [Custom.InstructorReviewed] = 'False'
          AND [System.CreatedDate] >= @Today - 60
          
          """
    })
    # Get the list of work items
    response = requests.post(url, headers=config.PRIMARY_HEADERS, data=payload, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch user stories. Error: {response.json()}")
        return []
    work_items = response.json()["workItems"]
    return work_items
    
# Function to fetch the details of a work item
# Function to fetch the details of a work item by its ID
def fetch_work_item_details(work_item_id):

    url = f"https://dev.azure.com/{config.DEVOPS_ORG}/_apis/wit/workitems/{work_item_id}"
    params = {"api-version":config.API_VERSION,
              "fields":"System.Description,Microsoft.VSTS.Common.AcceptanceCriteria,System.TeamProject"
              }
    response = requests.get(url, headers=config.PRIMARY_HEADERS,params=params)
    if response.status_code != 200:
        print(f"Failed to fetch work item details. Error: {response.json()}")
        return None
    return response.json()
    
class WorkItem(object):
    def __init__(self, id, description, acceptance_criteria):
        self.id = id
        self.description = description
        self.acceptance_criteria = acceptance_criteria
        self.feedback = None


def get_work_items_with_details():
    work_items = []

    # Get the list of work items
    for wid in fetch_open_user_stories():
        # Get the details of the work item
        id = wid.get("id")
        wid_details = fetch_work_item_details(id)
        
        # Gather the fields from the response
        _fields = wid_details.get('fields', {})
        description = _fields.get("System.Description","No description")
        acceptance_criteria = _fields.get("Microsoft.VSTS.Common.AcceptanceCriteria","No acceptance criteria")

        work_items.append(WorkItem(id, description, acceptance_criteria))
    
    return work_items


def get_chat_feedback(work_item):
    conversation= [
               {"role":"system", "content":config.BACKGROUND},
               {"role":"user", "content":work_item.description},
               {"role":"user", "content":work_item.acceptance_criteria}
    ]
    
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',messages=conversation)
    message = response['choices'][0]['message']['content']
    return message

def update_work_item(work_item_id, comment):
    url = f"https://dev.azure.com/{config.DEVOPS_ORG}/_apis/wit/workitems/{work_item_id}"

    headers = {
        'Content-Type': 'application/json-patch+json',
        'Authorization': f'Basic {config.DEVOPS_AUTH_TOKEN}',
    }
    params = {"api-version":config.API_VERSION}

    # Prepare the payload
    payload = [
        {
            "op": "add",
            "path": "/fields/System.History",
            "value": comment
        },
        {   "op": "add",
            "path": "/fields/Custom.AIReviewed",
            "value": "True"
        }
    ]
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(payload), params=params)

    if response.status_code == 200:
        print("Work item updated successfully.")
    else:
        print(f"Failed to update work item. Status code: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    openai.api_key = config.OPEN_API_KEY
    work_items = get_work_items_with_details()
    
    for work_item in tqdm.tqdm(work_items):
        feedback = get_chat_feedback(work_item)
        fixed_feedback = html.escape(feedback).replace('\n', '<br>')
        work_item.feedback = fixed_feedback
        update_work_item(work_item.id, fixed_feedback)
        
    json.dump([wi.__dict__ for wi in work_items], open("work_items.json","w"))
        