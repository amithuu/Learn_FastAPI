from fastapi import FastAPI,Body
from uuid import UUID
from datetime import datetime, time, timedelta
from typing import Optional

app=FastAPI()


@app.put('/items/{item_id}')
async def extra_data_types(
    item_id:UUID,
    start_date:Optional[datetime]=Body(None),
    end_date:Optional[datetime]=Body(None),
    repeat_at:Optional[time]=Body(None),
    process_after:Optional[timedelta]=Body(None),
    ):
    
    
    start_process = start_date + process_after
    duration = end_date - start_process
    
    return {
        'item_id':item_id,
        'start_date':start_date,
        'end_date':end_date,
        'repeat_at':repeat_at,
        'process_after':process_after,
        'start_process': start_process,
        'duration':duration,
    }
    
# ex:uuid4: 228e6ef4-dc04-4c01-836c-19a7ff17b29e