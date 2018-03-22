'''Example FSM diagram showing TDD workflow
'''
from fsm import FSM

fsm = FSM({
    'add'    ,
    'run'    ,
    'change' ,
    'rerun'  ,
})

fsm.transition ( 'add'    , 'run'    , 'new test'    )
fsm.fail       ( 'run'    , 'change' , 'test fails'  )
fsm.success    ( 'run'    , 'add'    , 'test passes' )
fsm.transition ( 'change' , 'rerun'  , 'alter code'  )
fsm.fail       ( 'rerun'  , 'change' , 'test fails'  )
fsm.success    ( 'rerun'  , 'add'    , 'tests pass'  )

fsm.save(name='tdd')
