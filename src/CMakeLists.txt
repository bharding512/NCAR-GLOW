cmake_minimum_required(VERSION 3.0)
project(GLOW
  LANGUAGES Fortran
  VERSION 0.981)
enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../cmake/Modules)

include(../cmake/compilers.cmake)

set(cglow_src glow.f90 cglow.f90 fieldm.f solzen.f90 ssflux.f90 rcolum.f90 qback.f90 etrans.f90 exsect.f gchem.f90 bands.f90 ephoto.f90 egrid.f90 maxt.f90)

set(snoem_src snoem.f90 snoemint.f90 geomag.f90)

set(utils_src mzgrid.f90 conduct.f90 nrlmsise00.f iri90.f)

add_library(cglow ${cglow_src} ${snoem_src} ${utils_src})
target_compile_options(cglow PRIVATE ${old})

# ------  Python Matlab command line driver -----------

add_executable(glow.bin glowpython.f90 utils.f90 fsutils.f90)
target_link_libraries(glow.bin cglow)
target_compile_options(glow.bin PRIVATE ${new})

# ------ MPI driver ------------
find_package(MPI COMPONENTS Fortran)
find_package(NetCDF)
if(MPI_Fortran_FOUND AND NetCDF_FOUND)
  add_executable(mpi_glow.bin glowdriver.f90 readtgcm.f90 output.f90 tzgrid.f90 fsutils.f90)
  target_link_libraries(mpi_glow.bin cglow MPI::MPI_Fortran NetCDF::NetCDF_Fortran)
  target_compile_options(mpi_glow.bin PRIVATE ${new})
endif()

#-------- tests --------------

find_package(Octave COMPONENTS Interpreter)
check_octave_source_runs("exit(exist('validateattributes'))")
if(OctaveOK)

add_test(NAME Simple COMMAND Octave::Interpreter --eval Simple
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/matlab)
set_tests_properties(Simple PROPERTIES TIMEOUT 20)

endif()
