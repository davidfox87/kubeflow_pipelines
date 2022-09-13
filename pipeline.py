import kfp
import kfp.components as comp
import kfp.dsl as dsl

import pandas as pd

read_op = kfp.components.load_component_from_file('component.yaml')
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


client = kfp.Client(host='http://localhost:8080')

# Compile, upload, and submit this pipeline for execution.
client.create_run_from_pipeline_func(my_pipeline, arguments={})