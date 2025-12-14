from airflow.sdk import dag, task, task_group

@dag
def task_grouping():

    @task
    def task1():
        return 5
    
    @task_group
    def task_grp1(val1):

        @task
        def task2(val2):
            return val2+5 #10

        @task
        def task3(val3):
            return val3+5 #15
        
        @task_group
        def nested_task_grp1(val4):

            @task
            def task4(val5):
                return val5+5 #20

            @task
            def task5(val6):
                return val6+5 #25
            
            return task5(task4(val4))
        
        return nested_task_grp1(task3(task2(val1)))
    

    @task
    def task6(val7):
        print("After all 5 tasks adding 5 for each task, the final value is",val7) #20
    
    task6(task_grp1(task1()))

task_grouping()