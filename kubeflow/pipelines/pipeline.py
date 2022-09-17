from kfp import dsl, Client, compiler


# EXPERIMENT_NAME = 'Simple notebook pipeline'        # Name of the experiment in the UI
# BASE_IMAGE = 'tensorflow/tensorflow:2.0.0b0-py3'    # Base image used for components in the pipeline

@dsl.component
def addition(num1: int, num2: int) -> int:
    return num1 + num2

@dsl.pipeline(
    name='My pipeline',
    description='My machine learning pipeline'
)
def my_pipeline(a: int = 1, b: int = 4):
    add_task_1 = addition(num1=a, num2=b)
    #add_task_2 = addition_component(num1=add_task_1.output, num2=c)

compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path=__file__ + '.yaml')


# kubeflow_gateway_endpoint="localhost:8080"
# kfp_client = Client(host=f"http://{kubeflow_gateway_endpoint}/pipeline")


# run = kfp_client.create_run_from_pipeline_func(my_pipeline,
#                                               arguments = {'a' : 1,
#                                                           'b' : 2
#                                               },
#                                               experiment_name=EXPERIMENT_NAME
#                                           )
# kubeflow_gateway_endpoint="localhost:8080"

# authservice_session_cookie="eyJfZnJlc2giOmZhbHNlLCJjc3JmX3Rva2VuIjoiNGVkMGQ2MzE3NDg1ZWZlMmJkNjRmNDU5OWVmM2I4ZDhmODIzZDg3NSJ9.YxF2oQ.7IVYbK_hwQuGFHVDuXyjpblqllk"

# namespace="kubeflow"

# client.list_experiments(namespace=namespace)

# Compile, upload, and submit this pipeline for execution.
#client.create_run_from_pipeline_func(my_pipeline, arguments={})