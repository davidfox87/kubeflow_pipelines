import kfp
import kfp.components as comp
import kfp.dsl as dsl
from kubernetes import client as k8s_client

import pandas as pd

read_op = kfp.components.load_component_from_file('components/my_first_component/component.yaml')
create_step_write_lines = comp.load_component_from_text("""
name: Write Lines
description: Writes text to a file.

inputs:
- {name: text, type: String}

outputs:
- {name: data, type: Data}

implementation:
  container:
    image: busybox
    command:
    - sh
    - -c
    - |
      mkdir -p "$(dirname "$1")"
      echo "$0" > "$1"
    args:
    - {inputValue: text}
    - {outputPath: data}
""")

def mnist_train_op(model_file, bucket):
    return dsl.ContainerOp(
      name="mnist_training_container",
      image='foxy7887/mnist_training_kf_pipeline:latest',
      command=['python', '/app/app.py'],
      file_outputs={'outputs': '/output.txt'},
      arguments=['--bucket', bucket, '--model_file', model_file]
    )

@dsl.pipeline(
  name='read pipeline',
  description='An example pipeline that performs file reading.'
)
def my_pipeline():
    write_lines_step = create_step_write_lines(
        text='one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten')

    get_lines_step = read_op(
        # Input name "Input 1" is converted to pythonic parameter name "input_1"
        input_1=write_lines_step.outputs['data'],
        parameter_1='5',
    )
    dsl.get_pipeline_conf()\
    .set_image_pull_secrets([k8s_client.V1ObjectReference(name="docker-hub-account")])


client = kfp.Client(host='http://localhost:8080/pipeline')

# Compile, upload, and submit this pipeline for execution.
client.create_run_from_pipeline_func(my_pipeline, arguments={})