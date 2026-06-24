## IMPORTS ##

# STANDARD LIBRARIES

# 3RD PARTY LIBRARIES
import pytest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from beam_constants import (
    MOCK_MESSAGE,
)
from btc_streaming_etl.dataflow.pipeline import (MessageDecoder, PipelineLogger)

# CUSTOM IMPORTS
##############


## Tests ##
def test_json_encoder(bytes_mock_message, encoded_mock_message):
    with TestPipeline() as pipeline:
        output = (
            pipeline
            | "Create Input Data" >> beam.Create([bytes_mock_message])
            | "Decode BTC Message" >> beam.ParDo(MessageDecoder())
            | "Log JSON Message" >> beam.ParDo(PipelineLogger())
        )
        assert_that(output, equal_to([encoded_mock_message]))

if __name__ == "__main__":
    None
else:
    None
