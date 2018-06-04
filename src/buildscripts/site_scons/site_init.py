import imp
import re
import os

# Some helper functions to get the correct version of a file
def get_src_file(file, env):
    return str(File(env.subst('$BASE_DIR') + "/" + file).srcnode().abspath)

def get_build_file(file, env):
    return str(File(env.subst('$BASE_DIR') + "/" + file).abspath)

def get_bin_file(file, env):
    return str(Dir(env.subst('$BIN_OUT')).abspath) + '/' + file

def get_lib_file(file, env):
    return str(Dir(env.subst('$LIB_OUT')).abspath) + '/' + file


# Get the variables from a .xxx_scons file
def get_var_from_file(filename):
    byteCompiledTempFile='tmpByteCode.py'
    fd = open(filename)
    data = imp.load_source('data', byteCompiledTempFile, fd)
    fd.close()
    try:
        os.remove(byteCompiledTempFile + 'c')
    except OSError:
        pass
    return data

    
# With a list of .dir_scons files it creates one list of singe_dirs
# one list of sub_dirs and one liste of ignore_dirs
def get_dirs_from_dir_files(dir_files, single_dirs, sub_dirs, ignore_dirs, env):
    # Read variable from the .dir_scons files
    for dir_file in dir_files:
        dir_file2 = env.subst('$BASE_DIR') + "/" + dir_file
        build_var = get_var_from_file(File(dir_file2).srcnode().abspath)
        single_dirs += Split(build_var.single_dirs)
        sub_dirs += Split(build_var.sub_dirs)
        ignore_dirs += Split(build_var.ignore_dirs)

# Creates a list of directories to search for based on the single, sub and ignore dir list
def get_dirs(single_dirs, sub_dirs, ignore_dirs, env):
    single_dirs2=[env.subst('$BASE_DIR') + "/" + s for s in single_dirs]
    ### Get sub_dirs
    sub_dirs2=[env.subst('$BASE_DIR') + "/" + s for s in sub_dirs]
    base_dir_src_abspath = Dir(env.subst('$BASE_DIR')).srcnode().abspath + '/'
    sub_dirs3 = []
    for dir in sub_dirs2:
        sub_dirs3.extend([x[0] for x in os.walk(Dir(dir).srcnode().abspath)])
    #### Add sub_dirs to singe_dirs
    for dir in sub_dirs3:
        single_dirs2.append(env.subst('$BASE_DIR') + "/" + str(dir).split(base_dir_src_abspath)[1])
    ### Remove any ignore_dirs
    ignore_dirs2=[env.subst('$BASE_DIR') + "/" + s for s in ignore_dirs]
    single_dirs3 = list(set(single_dirs2) - set(ignore_dirs2))
    return single_dirs3 
    
# Creates an object from a src file. .a files are just added as they are
def create_objs(srcs, env):
    ret_array = []
    for src in srcs:
        if re.match(".*\.a", src):
            ret_array.append(src)
        else:
            ret_array.append(env.Object(src))
    return ret_array

# Builds a binary from a .lnk_scons file
def build_lnk_scons(scons_dir, env):
    scons_files = Glob(scons_dir.path + '/' + '*.lnk_scons')
    for scons_file in scons_files:
        program_file = str(scons_file).split(".lnk_scons")[0]
        build_var = get_var_from_file(scons_file.srcnode().abspath)
        src_files = Split(build_var.src_files)
        src_files2=[env.subst('$BASE_DIR') + "/" + s for s in src_files]
        obj_files2 = create_objs(src_files2, env)
        libs = Split(build_var.libs)
        executable=env.Program(program_file, obj_files2, LIBS=libs)
        env.Install(env['BIN_OUT'], executable)
        program_name = program_file.split("/")[-1] 
        env.Alias(program_name, get_bin_file(program_name, env))
    
# Builds a library from a .lib_scons file
def build_lib_scons(scons_dir, env):
    scons_files = Glob(scons_dir.path + '/' + '*.lib_scons')
    for scons_file in scons_files:
        lib_file = str(scons_file).split(".lib_scons")[0]
        build_var = get_var_from_file(scons_file.srcnode().abspath)
        src_files = Split(build_var.src_files)
        src_files2=[env.subst('$BASE_DIR') + "/" + s for s in src_files]
        obj_files2 = create_objs(src_files2, env)
        lib = env.Library(lib_file, obj_files2)
        env.Install(env['LIB_OUT'], lib)
        lib_name = lib_file.split("/")[-1]
        env.Alias('lib' + lib_name, get_lib_file('lib' + lib_name + '.a', env))

# Executes a .bld_scons file
def build_bld_scons(scons_dir, env):
    scons_files = Glob(scons_dir.path + '/' + '*.bld_scons')
    for scons_file in scons_files:
        SConscript(scons_file, exports='env')

# Builds lnk_scons and lib_scons files
def build_scons_files(scons_dir, env):
    build_lnk_scons(scons_dir, env)
    build_lib_scons(scons_dir, env)
    build_bld_scons(scons_dir, env)

# External function called from the SConstruct file
def build_scons_from_dir_files(dir_files, env):
    dir_files2 = Split(dir_files)
    single_dirs = []
    sub_dirs = []
    ignore_dirs = []
    get_dirs_from_dir_files(dir_files2, single_dirs, sub_dirs, ignore_dirs, env)
    for dir in get_dirs(single_dirs, sub_dirs, ignore_dirs, env):
        build_scons_files(Dir(dir), env)
        
              