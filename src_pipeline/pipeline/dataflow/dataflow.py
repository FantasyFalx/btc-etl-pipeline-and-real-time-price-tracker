"""File for creating the dataflow pipeline"""
# Standard libraries:
import json
from collections import Counter
import logging
# 3rd Party: 
import apache_beam as beam
# For GCP Production use ---------------------------
from apache_beam.io.gcp.pubsub import ReadFromPubSub
## ------------------------------------------------
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam import window
import numpy as np
# Custom Libraries
from configs.configs import TABLE_SCHEMA, OUTPUT_TABLE, TOPIC, PIPELINE_OPTIONS, SUBSCRIPTION

# Pipeline Functions for data transformations
def json_converter(data: dict):
    return json.loads(data)

class Logger(beam.DoFn):
    def process(self, element):
        logging.info(f"Incoming element: {element}")
        yield element

class Converter(beam.DoFn):
    def process(self, element: dict):
        for key, value in element.items():
            if key == "api_url":
                continue
            else:
                yield (key, value)
            
class Aggregator(beam.DoFn): 
    
    def process(self, element):
        key, value = element
        
        try:
            if key == "btc_price":
                min_price = ("btc_min_price", min(value))
                max_price = ("btc_max_price", max(value))
                average_price = ("btc_average_price", round(sum(value) / len(value)))
                price_change = ("btc_price_change", len(value))
                yield (key, value)
                yield min_price
                yield max_price
                yield average_price
                yield price_change
            yield(key, value[0])
        
        except ValueError as v:
            logging.error("Error: %s, skipping incorrect value type.", v) 
        except IndexError as i:
            logging.error("Error: %s, skipping non existent index value.", i) 
        except TypeError as t:
            logging.error("Error: %s, skipping empty data type.", t) 

        
class FilterNoneDict(beam.DoFn):
    def process(self, element):
        if element == {}:
            pass
        else:
            yield element
         
# Main Data Pipeline            
def pipeline_runner() -> None: 
    
    options = PipelineOptions(flags=["--dataflow_service_options=enable_preflight_validation=false"], **PIPELINE_OPTIONS)
    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as btc_pipeline:
         
        streaming_data = (
           btc_pipeline 
            | "Gets the pub/sub message." >> beam.io.ReadFromPubSub(subscription=SUBSCRIPTION).with_output_types(bytes)
            | "Decodes the BTC pub/sub message data." >> beam.Map(lambda x: x.decode('utf-8')) 
            |  "Create a dict object from a python object" >> beam.Map(json_converter)
            | "Log 1" >> beam.ParDo(Logger())
            | "Creates a window for the pub/sub data set to 60 seconds." >> beam.WindowInto(
                    window.FixedWindows(60),
                    allowed_lateness=(1 * 5)
            )
           | "Par do" >> beam.ParDo(Converter())
           | "Log 2" >> beam.ParDo(Logger())
        )
        
        
        aggregated_data = (
            streaming_data | "Group by key function" >> beam.GroupByKey()
            | "Log 3" >> beam.ParDo(Logger())
            |"Aggregate the btc price metrics." >> beam.ParDo(Aggregator())
            | "Log 4" >> beam.ParDo(Logger())
            | "to dict" >> beam.combiners.ToDict().without_defaults() # Does not set a dictionary default. 
            | "Log 5" >> beam.ParDo(Logger())
            | "Filters the none Dicts" >> beam.ParDo(FilterNoneDict())
            | "Log 6" >> beam.ParDo(Logger())
        )
        
        aggregated_data | "Appends btc streaming data to bigquery table." >> beam.io.WriteToBigQuery(
                table=OUTPUT_TABLE,
                schema=TABLE_SCHEMA,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
        # -----------------------------------------------------------------------
                    
if __name__ == "__main__":
    # Local Runner for testing purposes
    pipeline_runner()

 
