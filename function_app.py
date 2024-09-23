import logging
import azure.functions as func
import config
import openai
from story_feedback import get_work_items_with_details, get_chat_feedback, update_work_item
from datetime import datetime
import json
import html

app = func.FunctionApp()

@app.schedule(schedule="0 0 */4 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timed_story_feedback(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function started.')
    openai.api_key = config.OPEN_API_KEY
    work_items = get_work_items_with_details()
    
    for work_item in work_items:
        logging.debug(f'Processing work item {work_item.id}')
        feedback = get_chat_feedback(work_item)
        fixed_feedback = html.escape(feedback).replace('\n', '<br>')
        work_item.feedback = fixed_feedback
        update_work_item(work_item.id, fixed_feedback)
        logging.debug(f"Work item {work_item.id} updated.")
        
    now = datetime.now().strftime('%m%d%H%M')
    json.dump([wi.__dict__ for wi in work_items], open(f"work_items{now}.json","w"))
    