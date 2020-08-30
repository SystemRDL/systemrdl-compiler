from typing import TYPE_CHECKING, List

from antlr4 import InputStream

from .perl_preprocessor import PerlPreprocessor

if TYPE_CHECKING:
    from .segment_map import SegmentMap
    from ..compiler import RDLEnvironment

class PreprocessedInputStream(InputStream):
    def __init__(self, data: str, seg_map: 'SegmentMap'):
        super().__init__(data)
        self.seg_map = seg_map

def preprocess_file(env: 'RDLEnvironment', path: str, search_paths: List[str]) -> PreprocessedInputStream:
    # Run file through Perl preprocessor
    ppp = PerlPreprocessor(env, path, search_paths)
    preprocessed_text, seg_map = ppp.preprocess()

    # Encapsulate into an Antlr-like input stream object
    input_stream = PreprocessedInputStream(preprocessed_text, seg_map)
    return input_stream
