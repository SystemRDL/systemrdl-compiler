from antlr4 import InputStream

from .perl_preprocessor import PerlPreprocessor

class PreprocessedInputStream(InputStream):
    def __init__(self, data, seg_map):
        super().__init__(data)
        self.seg_map = seg_map

def preprocess_file(env, path: str, search_paths) -> PreprocessedInputStream:
    # Run file through Perl preprocessor
    ppp = PerlPreprocessor(env, path, search_paths)
    preprocessed_text, seg_map = ppp.preprocess()

    # Encapsulate into an Antlr-like input stream object
    input_stream = PreprocessedInputStream(preprocessed_text, seg_map)
    return input_stream
