# ideas

# structure

1. vue
   - UI
      - vuexy + vutify
   - router
      - vue-router
   - js+ts
2. back_end
   - fastapi
      - middleware + typecheck + complex operation
   - supabase-py
      - async_client interact with supabase online
   - metabase
      - data analysis connected to supabase online
      - data cleaning scripts such as combining alipay and wechatpay bills
   - backup
      - sqlite to store data locally according to the data from supabase

# functions

1. vue
   - task_done_list
      - CRUD operations to record tasks

# components

1. vue
   - task_done_list
      - table
      - dialog to manage tasks
      - dialog to manage task categories

# TODO

1. TaskDoneManagement.js => TaskDoneManagement.ts
2. construct backup sqlite database from supabase
3. sync finance data from bill.csv to supabase
4. construct finance analysis on vue
5. scrapy to get alipay bill

# Questions

1. A task may take multiple times to complete, which means that only part of the progress can be completed each time.
2. It is necessary to propose a to-do function, preferably with a reminder and a deadline.
3. A task may be divided into multiple completion periods, or only the total time taken may be recorded, and the
   complete period cannot be recorded.
