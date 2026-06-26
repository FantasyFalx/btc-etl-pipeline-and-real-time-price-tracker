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
from btc_streaming_etl.dataflow.pipeline import (
    MessageDecoder, PipelineLogger, JsonDecoder)

# CUSTOM IMPORTS
##############

## Tests ##
def test_json_decoder(bytes_mock_message):
    with TestPipeline() as pipeline:
        output = (
            pipeline
            | "Create Input Data" >> beam.Create([bytes_mock_message])
            | "Decode BTC Message" >> beam.ParDo(MessageDecoder())
            | "Log JSON Message" >> beam.ParDo(PipelineLogger())
            | "Encode JSON Message" >> beam.ParDo(JsonDecoder())
        )
        assert_that(output, equal_to([MOCK_MESSAGE]))

if __name__ == "__main__":
    None
else:
    None
