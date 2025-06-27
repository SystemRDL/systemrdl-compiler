import os

from systemrdl import RDLCompiler

from function_profiler import Profiler

# Collect list of files
this_dir = os.path.dirname(os.path.realpath(__file__))
files = []
with open(os.path.join(this_dir, "../accellera-examples/all.f"), 'r') as f:
    for line in f.readlines():
        line = line.strip()
        path = os.path.join(this_dir, "../accellera-examples", line)
        files.append(path)

def code_to_profile():
    rdlc = RDLCompiler(single_elaborate_optimization=True)
    for input_file in files:
        rdlc.compile_file(input_file)
    root = rdlc.elaborate()

# Bind profiling timers to specific parts of the compiler
profiler = Profiler()
profiler.bind_timer(__name__, "code_to_profile", "Total")
profiler.bind_timer("systemrdl.preprocessor", "preprocess_file", "preprocess")
profiler.bind_timer("systemrdl.parser.sa_systemrdl", "parse", "lex/parse")
profiler.bind_timer("systemrdl.core.ComponentVisitor", "RootVisitor.visitRoot", "compile")
profiler.bind_timer("systemrdl.compiler", "RDLCompiler.elaborate", "elaborate")

profiler.bind_timer("systemrdl.component", "Component._copy_for_inst", "comp deepcopies")

# Run!
code_to_profile()

# Display results
profiler.print_result()
