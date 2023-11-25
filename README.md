# ideas
## 设计理念

1. **数据驱动决策**  
   利用详细的任务记录和分析，使决策过程更加依赖于实际数据，从而提高效率和效果。

2. **灵活的分析方案**  
   用户自定义分析方案，根据个人需求和偏好分析任务数据。

3. **简化任务记录**  
   通过模板系统减少手动输入，使任务记录更加高效和准确。

4. **多维标签和分类**  
   为任务提供多重标签和分类，以支持更复杂的数据分析和报告生成。

## 主要功能

1. **详细任务记录**  
   记录任务的每个细节，如时间、地点、具体内容等。

2. **自动化标签和分类**  
   通过预设模板系统自动添加标签和分类，减少手动输入。

3. **自定义分析工具**  
   提供工具供用户自定义任务数据的分析方式。

4. **自动生成报告**  
   利用GPT-4接口自动生成周报和月报，基于任务数据提供总结和分析。

5. **进度跟踪**  
   在模板中仅需更新任务进度，自动记录详细信息。

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

