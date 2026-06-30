# Standard libraries:
import argparse
import logging

# 3rd Party:
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions

# Custom Libraries
from btc_streaming_etl.dataflow.configs.configs import (
    TABLE_SCHEMA,
    OUTPUT_TABLE,
    PIPELINE_OPTIONS,
    SUBSCRIPTION,
)

class MessageDecoder(beam.DoFn):
    def process(self, element: bytes):
        yield element.decode('utf-8')

class PipelineLogger(beam.DoFn):
    def process(self, element):
        logging.info(f"Incoming BTC pub/sub message: {element}")
        yield element

class JsonDecoder(beam.DoFn):
    def process(self, element):
        yield json.loads(element)

def pipeline_runner(argv=None) -> None:
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subscription", default=SUBSCRIPTION)
    parser.add_argument("--output", default=OUTPUT_TABLE)
    template_args, pipeline_args = parser.parse_known_args(argv)

    flag = "--dataflow_service_options=enable_preflight_validation=false"
    options = PipelineOptions(pipeline_args, flags=[flag])
    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as btc_pipeline:

        streaming_data = (
            
            btc_pipeline
            | "Extracts the pub/sub message."s
            >> beam.io.ReadFromPubSub(
                subscription=template_args.subscription
            ).with_output_types(
                bytes
            )
            | "Decodes the BTC pub/sub message data." >> beam.ParDo(
                MessageDecoder()
            )
            | "Logs current processed message to the console." >> beam.ParDo(
                PipelineLogger()
            )
            | "Logs current JSON encoded message to the console." >> beam.ParDo(
                PipelineLogger()
            )
            | "Decodes the JSON message to a dictionary." >> beam.ParDo(
                JsonDecoder()
            )
        )

        streaming_data | "Appends messages to BigQuery table." >> beam.io.WriteToBigQuery(
            table=template_args.output,
            schema=TABLE_SCHEMA,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        )


if __name__ == "__main__":
    pipeline_runner()
else: 
    None
