import kfp
import kfp.components as comp
import kfp.dsl as dsl
from kubernetes import client as k8s_client
import kfp.aws as aws

import pandas as pd
S3_BUCKET = 'my_bucket'

def mnist_train_op(model_file, bucket):
    return dsl.ContainerOp(
      name="mnist_training_container",
      image='foxy7887/mnist_training_kf_pipeline:latest',
      command=['python', '/app/app.py'],
      file_outputs={'outputs': '/output.txt'},
      arguments=['--bucket', bucket, '--model_file', model_file]
    )


# Define the pipeline
@dsl.pipeline(
   name='Mnist pipeline',
   description='A toy pipeline that performs mnist model training.'
)
def mnist_container_pipeline(
    model_file: str = 'mnist_model.h5', 
    bucket: str = S3_BUCKET
):
    mnist_train_op(model_file=model_file, bucket=bucket).apply(
                      aws.use_aws_secret('aws-secret', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'us-west-1'))



client = kfp.Client(host='http://localhost:8080/pipeline')


experiment_name = 'minist_kubeflow'

arguments = {"model_file":"mnist_model.h5",
             "bucket":S3_BUCKET}

pipeline_func = mnist_container_pipeline

run_name = pipeline_func.__name__ + ' run'

# Submit pipeline directly from pipeline function
run_result = client.create_run_from_pipeline_func(pipeline_func, 
                                                  experiment_name=experiment_name, 
                                                  run_name=run_name, 
                                                  arguments=arguments)


