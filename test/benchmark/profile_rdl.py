import cProfile
import pstats
import os

from systemrdl import RDLCompiler

# Collect list of files
this_dir = os.path.dirname(os.path.realpath(__file__))
files = []
with open(os.path.join(this_dir, "../accellera-examples/all.f"), 'r') as f:
    for line in f.readlines():
        line = line.strip()
        path = os.path.join(this_dir, "../accellera-examples", line)
        files.append(path)

# Run profiler
profiler = cProfile.Profile()
with profiler:
    rdlc = RDLCompiler()
    for input_file in files:
        rdlc.compile_file(input_file)
    root = rdlc.elaborate()

# Extract stats
stats = pstats.Stats(profiler)
stats.sort_stats("cumtime")
stats_profile = stats.get_stats_profile()

# Get stats for notable parts of the compile flow
t_total = stats_profile.total_tt
for func_name, func_profile in stats_profile.func_profiles.items():
    #print(f"{func_profile.cumtime:3.4f} {func_name:10s} - {func_profile.file_name}")
    if func_profile.file_name.endswith("preprocessor/__init__.py") and func_name == "preprocess_file":
        t_preprocess = func_profile.cumtime
    elif func_profile.file_name.endswith("sa_systemrdl.py") and func_name == "_cpp_parse":
        t_parse = func_profile.cumtime
    elif func_profile.file_name.endswith("ComponentVisitor.py") and func_name == "visitRoot":
        t_compile = func_profile.cumtime
    elif func_profile.file_name.endswith("systemrdl/component.py") and func_name == "_copy_for_inst":
        t_copy_for_inst = func_profile.cumtime
    elif func_profile.file_name.endswith("systemrdl/compiler.py") and func_name == "elaborate":
        t_elaborate = func_profile.cumtime

print(f"preprocess:      {100 * t_preprocess / t_total:.1f}%")
print(f"parse:           {100 * t_parse / t_total:.1f}%")
print(f"compile:         {100 * t_compile / t_total:.1f}%")
print(f"elaborate:       {100 * t_elaborate / t_total:.1f}%")
print(f"inst deepcopies: {100 * t_copy_for_inst / t_total:.1f}%")
