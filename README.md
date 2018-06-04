# Scons Embedded Build (seb)
-----------------------------


## A wrapper for scons build
The Scons Embedded Build is a set of scons scripts that makes
it easy to compile the same code for different CPUs.

Scons is very good on the dependency handling, but it mixes
to much of How to compile with What to compile.


## What I want!
I want the following from a build system
* Build is separated from source
* For every executable I only specify which source files I need
* Compiler and compiler options are in one place per build target
* Can specify which directories to include for each build target
* Possible to make custom build scripts that understands dependencies
* Only build what needs to be built


## Build the x86_64 world!
Lets create the x86_64 build directory and build it

```console
$ cd ..
$ mkdir x86_64
$ cd x86_64
$ ln -s ../seb/src/buildscripts/SConstruct_x86_64 SConstruct
$ ln -s ../seb/src/buildscripts/site_scons/ 
$ scons
```

You should get something like this

```console
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
build/src/vehicle/bus/bus.cpp -> build/src/vehicle/bus/bus.o
build/src/vehicle/apps/engine/Engine.cpp -> build/src/vehicle/apps/engine/Engine.o
build/src/vehicle/apps/engine/EngineBlock.cpp -> build/src/vehicle/apps/engine/EngineBlock.o
build/src/vehicle/apps/engine/Piston.cpp -> build/src/vehicle/apps/engine/Piston.o
build/src/vehicle/apps/engine/Engine.o build/src/vehicle/apps/engine/EngineBlock.o build/src/vehicle/apps/engine/Piston.o -> build/src/vehicle/apps/engine/libengine.a
build/src/vehicle/apps/engine/Engine.o build/src/vehicle/apps/engine/EngineBlock.o build/src/vehicle/apps/engine/Piston.o -> build/src/vehicle/apps/engine/libengine.a
Install file: "build/src/vehicle/apps/engine/libengine.a" as "lib/libengine.a"
build/src/vehicle/bus/bus.o -> build/src/vehicle/bus/bus
Install file: "build/src/vehicle/bus/bus" as "bin/bus"
../seb/src/buildscripts/codegen.py /tmp/scons/seb/src/vehicle/apps/window /tmp/scons/x86_64/build/src/vehicle/apps/window
build/src/vehicle/car/car.cpp -> build/src/vehicle/car/car.o
build/src/vehicle/apps/wheel/Wheel.cpp -> build/src/vehicle/apps/wheel/Wheel.o
build/src/vehicle/apps/window/Front.gen.cpp -> build/src/vehicle/apps/window/Front.gen.o
build/src/vehicle/car/car.o build/src/vehicle/apps/wheel/Wheel.o build/src/vehicle/apps/window/Front.gen.o -> build/src/vehicle/car/car
Install file: "build/src/vehicle/car/car" as "bin/car"
scons: done building targets.

```

Rebuilding it by executing *scons* again will show that it is up to date.

You can execute the compiled programs
```console
$ ./bin/car 
I am a car with wheels size 9 and engine power 160
My front window is blank
$ ./bin/bus
I am a bus without engine power 1200
```


## Files

### .lnk_scons
This is the linker file that tells which source files
and libraries that are needed for an executable.
This is the *src/vehicle/car/car.lnk_scons* file


```python
src_files = ("""    
   src/vehicle/car/car.cpp
   src/vehicle/apps/wheel/Wheel.cpp
   src/vehicle/apps/window/Front.gen.cpp
""")

libs = ("""
    engine
""")
```

### .lib_scons
This is a linker file for a library


```python
src_files = ("""    
   src/vehicle/apps/engine/Engine.cpp
   src/vehicle/apps/engine/EngineBlock.cpp
   src/vehicle/apps/engine/Piston.cpp
""")
```

### .bld_scons
This is generic build script. It executes as a Python script and
can take any files as input and generate one or more outputs.
You can use this for automatic code generation or more complex
compilations. Below is the window.bld_scons 

```python
Import('env')

# This build rule uses 4 .cfg files to generate 4 .gen.h and 4 gen.cpp files
# the codegen.py script which is given in the env['CODEGEN'] is just a
# dummy program. In real life this could some automatic code generation.


# We need to create a list of all the inputfiles that the codegen.py reads
# and all the ouputs it generates. This is used for the scons dependencies

sides = ['Front', 'Left', 'Right', 'Back']
inputfiles = []
outputfiles = []
for side in sides:
    inputfiles += [side.lower() + '.cfg']
    outputfiles += [side + '.gen.h']
    outputfiles += [side + '.gen.cpp']

# We need the absolute input directory which is in the src area
# and the absolute output directory which is in the build area
# so that codegen.py read and write from the correct location
inputdir =  str(Dir(env.subst('$BASE_DIR') + "/" + 'src/vehicle/apps/window/').srcnode().abspath)
outputdir = str(Dir(env.subst('$BASE_DIR') + "/" + 'src/vehicle/apps/window/').abspath)

# Create the command that will be executed by scons
cmd = env['CODEGEN'] + ' ' + inputdir + ' ' + outputdir

# Scons will execute the command 'cmd' and use to list of
# outputfiles and inputfiles to get the dependencies correct
env.Command(outputfiles, inputfiles, cmd)
```

The last *env.Command* takes arrays for the input and output files
and the command to execute. Besides that you can do what you want.



### .dir_scons
This is a list of directories that shall be searched for *.xxx_scons* files
It is possible to specify single directories, a directory with all 
sub-directories and even ignore any special directories

You can typically have some files that are common for all Linux targets
but put all the host test in a separate .dir_scons that is only picked
up by your x86_64 host build.


```python
# Scons build will pick up all files in single_dirs
# but not any sub directories
single_dirs = ("""
    
""")

# Scons will pick up all files in sub_dirs and
# also all sub directories 
sub_dirs = ("""
    src/vehicle
""")

# It is possible to ignore special directories that has 
# been picked up by the general sub_dirs
ignore_dirs = ("""
    src/vehicle/apps/broken
""")    
```

In this example we want to ignore the *broken* directories since it
does not compile

### SConstruct_xxx
Scons requires that there is a *SConstruct* file in the directory you
run scons from. To be able to have different SConstruct files stored
in git I use a _xxx extension to separate them, and a symbolic link to
make scons happy.

The following is the SConstruct_ppc440. The SConstruct_ppc440 is similar
but for native host we don't need to specify the compiler


```python
# Get the environment
env = Environment()

# Get argument for the verbose output
AddOption('--verbose',
          action="store_true", 
          dest="verbose",
          default=False,
          help='Verbose compile output')

# Compile output format
if not GetOption('verbose'):
    env['CCCOMSTR'] = "$SOURCES -> $TARGET"
    env['CXXCOMSTR'] = "$SOURCES -> $TARGET"
    env['ARCOMSTR'] = "$SOURCES -> $TARGET"
    env['ASCOMSTR'] = "$SOURCES -> $TARGET"
    env['ASPPCOMSTR'] = "$SOURCES -> $TARGET"
    env['LDMODULECOMSTR'] = "$SOURCES -> $TARGET"
    env['LINKCOMSTR'] = "$SOURCES -> $TARGET"
    env['RANLIBCOMSTR'] = "$SOURCES -> $TARGET"
    
    
# Common variables for all types of build
env.VariantDir('build', '../seb')
env.Append(CPPPATH=['#build'])
env.Append(LIBPATH = '#lib')
env.Append(BASE_DIR=['#build'])
env.Append(BIN_OUT = '#bin')
env.Append(LIB_OUT = '#lib')

# Compiler setup
env.Replace(CC    = 'powerpc-linux-gnu-gcc')
env.Replace(CXX   = 'powerpc-linux-gnu-g++')
env.Replace(LD    = 'powerpc-linux-gnu-ld') 
env.Replace(AR    = 'powerpc-linux-gnu-ar') 
env.Replace(STRIP = 'powerpc-linux-gnu-strip') 

# We use a dummy program to do some automatic code generation
env.Replace(CODEGEN = '../seb/src/buildscripts/codegen.py')

# Compile flags
env.Append(CCFLAGS = ['-Wall', '-Wextra', '-O2'])

# Link flags
env.Append(LINKFLAGS = '-s')

# Build defines
env.Append(CPPDEFINES=['FOO_PPC'])

# List all .dir_scons files for this build
dir_files = ("""
    src/buildscripts/linux.dir_scons
""")

# Build everything
build_scons_from_dir_files(dir_files, env)
```


### site_scons/site_init.py
The *site_scons* directory contains the *site_init.py* script. Scons will look
for this in build directory and automatically read it. The file contains
the function build_scons_from_dir_files() which starts the build


## Build the ppc440 world!
Before you can build for ppc440 you need to install the compiler
```console
$ sudo apt-get install gcc-powerpc-linux-gnu
$ sudo apt-get install g++-powerpc-linux-gnu
```

Now you can build it the same way as for x86_64
```console
$ cd ..
$ mkdir ppc440
$ cd ppc440
$ ln -s ../seb/src/buildscripts/SConstruct_ppc440 SConstruct
$ ln -s ../seb/src/buildscripts/site_scons/ 
$ scons
```


## What do I have to do to make it work for me?
If your source is not in "src" you need to change the "../seb" in the SConstruct file
Most likely there is also more....

