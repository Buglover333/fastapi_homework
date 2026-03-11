from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    task_text: str
    task_id: Optional[int] = None
    task_deadline: Optional[datetime] = None
    
    @field_validator('task_deadline')
    def validate_deadline(cls, v):
        if v is not None and v < datetime.now():
            raise ValueError('Ты дебил? Схера-ли у тебя ДЕДЛАЙН стоит В ПРОШОМ???')
        return v

# типо котик ищет баги
#        _                        
#        \`*-.                    
#         )  _`-.                 
#        .  : `. .                
#        : _   '  \               
#        ; *` _.   `*-._          
#        `-.-'          `-.       
#          ;       `       `.     
#          :.       .        \    
#          . \  .   :   .-'   .   
#          '  `+.;  ;  '      :   
#          :  '  |    ;       ;-. 
#          ; '   : :`-:     _.`* ;
# [bug] .*' /  .*' ; .*`- +'  `*' 
#       `*-*   `*-*  `*-*'
