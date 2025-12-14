import warnings
from typing import Callable, ClassVar, Collection, Mapping, Any
from collections.abc import Sequence
from airflow.sdk.bases.decorator import DecoratedOperator,TaskDecorator,task_decorator_factory
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.definitions._internal.types import SET_DURING_EXECUTION
from airflow.utils.context import context_merge
from airflow.utils.operator_helpers import determine_kwargs
from airflow.sdk.definitions.context import Context



class _SQLDecoratedOperator(DecoratedOperator, SQLExecuteQueryOperator):

    template_fields : Sequence[str]= (*DecoratedOperator.template_fields, *SQLExecuteQueryOperator.template_fields)
    template_fields_renderers: ClassVar[dict[str,str]] ={
        **DecoratedOperator.template_fields_renderers,
        **SQLExecuteQueryOperator.template_fields_renderers
    }

    custom_operator_name : str = "@task.sql" #we defined how we want to use the "_SQLDecoratedOperator" decorator in our dags using the name of the decorator  
    overwrite_rtif_after_execution: bool = True #attribute related to templated fields

    def __init__(self, * , python_callable:Callable, op_args: Collection[Any]| None = None,
                  op_kwargs: Mapping[str,Any]| None = None, **kwargs) ->None:
        #parameters we have for the python operator, because behidn the scene task decorator is python operator and we are wrapping the SQLExecuteQueryOperator in a python operator.
        if(kwargs.pop("multiple_outputs",None)):
            warning.warn(
                f"`multiple_outputs=True` is not supported in (self.custom_operator_name) tasks.Ignoring.",
                UserWarning,
                stacklevel = 3
            )
        super().__init__(python_callable=python_callable,op_args=op_args,op_kwargs=op_kwargs,
                         sql=SET_DURING_EXECUTION, multiple_outputs = False,
                         **kwargs) #initialize the parent class 
        
    def execute(self,context:Context)->Any: #this function is executed as soon as the task runs in the airflow
        # so when we run a task in airflow that task has a task instance, context attached to it

        context_merge(context, self.op_kwargs)
        kwargs = determine_kwargs(self.python_callable, self.op_args, context)

        #sql request that we want to execute to the following value and _SQLDecoratedOperator is a decorator
        # we are gonna execute python callable function so the python functon that will be decorated and that function returns the sql query that we want to execute
        self.sql = self.python_callable(*self.op_args, **kwargs)
        
        if(not isinstance(self.sql,str) or self.sql.strip()==""):
            raise TypeError("The returned value from the taskFlow callable must be a non-empty string.")

        context['ti'].render_templates() #rendering the templates

        return super().execute(context) # we want to execute the SQL query with SQLExecuteQueryOperator and we are passing the context to the parent class 


#new python function corresponding to my decorator
def sql_task(python_callable:Callable | None = None, **kwargs)->TaskDecorator:
    return task_decorator_factory(
        python_callable=python_callable,
        decorated_operator_class = _SQLDecoratedOperator,
        **kwargs
    )
    