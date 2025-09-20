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
    rdlc = RDLCompiler()
    for input_file in files:
        rdlc.compile_file(input_file)
    root = rdlc.elaborate()

# Bind profiling timers to specific parts of the compiler
profiler = Profiler()
profiler.bind_timer(__name__, "code_to_profile", "Total")
profiler.bind_timer("systemrdl.preprocessor", "preprocess_file", "preprocess")
profiler.bind_timer("systemrdl.parser.sa_systemrdl", "parse", "lex/parse")
profiler.bind_timer("systemrdl.core.ComponentVisitor", "RootVisitor.visitRoot", "compile")
profiler.bind_timer("systemrdl.compiler", "RDLCompiler.elaborate", "elaborate total")
profiler.bind_timer("systemrdl.compiler", "RDLCompiler._elab_create_root_inst", "elaborate-inst")
profiler.bind_timer("systemrdl.compiler", "RDLCompiler._elab_design", "elaborate-expr")
profiler.bind_timer("systemrdl.compiler", "RDLCompiler._elab_validate", "validate")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.enter_Component"            , "validate:enter_Component           ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.enter_Signal"               , "validate:enter_Signal              ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.enter_AddressableComponent" , "validate:enter_AddressableComponent")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.enter_Addrmap"              , "validate:enter_Addrmap             ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.enter_Reg"                  , "validate:enter_Reg                 ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.exit_Reg"                   , "validate:exit_Reg                  ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.enter_Field"                , "validate:enter_Field               ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.exit_Field"                 , "validate:exit_Field                ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.exit_Regfile"               , "validate:exit_Regfile              ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.exit_Addrmap"               , "validate:exit_Addrmap              ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.exit_Mem"                   , "validate:exit_Mem                  ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.exit_AddressableComponent"  , "validate:exit_AddressableComponent ")
#profiler.bind_timer("systemrdl.core.validate", "ValidateListener.exit_Component"             , "validate:exit_Component            ")
#profiler.bind_timer("systemrdl.node", "Node.get_property" , "Node.get_property")

# Run!
code_to_profile()

# Display results
profiler.print_result()
