from airflow.sdk import dag, task, task_group
from airflow.models.param import Param
from airflow.utils.trigger_rule import TriggerRule

@dag(
        params ={
            "X":Param(5,type="integer",description="Enter the value of X"),
            "Y":Param(5,type="integer",description = "Enter the value of Y")
        }
)
def Branching():

    @task
    def input_values(**context):
        X = context["params"]["X"]
        Y = context["params"]["Y"]
        return {
            "X":X,
            "Y":Y,
            "Summation":X+Y
        }
    
    @task.branch
    def branching_condition(val):
        if(val["Summation"]>10):
            return "greater_than_10"
        else:
            return "less_or_equal_10"
    
    @task.branch
    def greater_than_10(val):
        if(val["Summation"]%2==0):
            return "evn_or_odd_grp.even"
        else:
            return "evn_or_odd_grp.odd"

        
    @task.branch
    def less_or_equal_10(val):
        if(val["Summation"]%2==0): # the condition in if fails then there is no else statement then it will none if there none the downstream tasks skips
            return "evn_or_odd_grp.even"
        else:
            return "evn_or_odd_grp.odd"

    
    @task_group
    def evn_or_odd_grp(val1):

        @task(
                trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
        )
        def even(val2):
            print(f"Given Summation of values {val2["X"]} and {val2["Y"]} is {val2["Summation"]} which is also an Even number")

        @task(
                trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
        )
        def odd(val3):
            print(f"Given Summation of values {val3["X"]} and {val3["Y"]} is {val3["Summation"]} which is also an Odd number")
        
        even(val1) 
        odd(val1)
    
    #we are calling the task once (instantiate tasks exactly once)
    val = input_values()
    main_branch = branching_condition(val)
    branch_greater_10 = greater_than_10(val)
    branch_less_equal_10 = less_or_equal_10(val)
    even_or_odd = evn_or_odd_grp(val)

    main_branch >> [branch_greater_10,branch_less_equal_10] >> even_or_odd

Branching()