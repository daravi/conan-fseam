import os
import glob

from conans import ConanFile, CMake, tools

class FSeam(ConanFile):
    name = "fseam"
    project = "FSeam"
    description = "Header only library to manage compile time mock class"
    topics = ("conan", "fseam", "header-only", "unit-test", "tdd", "seaming")
    homepage = "https://github.com/FreeYourSoul/FSeam"
    license = "MIT"
    exports_sources = ["patches/*"]
    settings = "os", "compiler", "build_type", "arch"
    options = {"use_gtest": [True, False]}
    default_options = {"use_gtest": True}
    generators = ["cmake", "cmake_find_package"]

    _cmake = None
    
    @property
    def _source_subfolder(self):
        return "source_subfolder"
    @property
    def _build_subfolder(self):
        return "build_subfolder"
    
    def requirements(self):
        if self.options.use_gtest:
            self.requires("gtest/1.10.0")
        else:
            self.requires("catch2/2.13.0")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = glob.glob("{}-*".format(self.project))[0]
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        cmake = CMake(self)
        cmake.definitions["FSEAM_USE_CATCH2"] = not self.options.use_gtest
        cmake.definitions["FSEAM_USE_GTEST"] = self.options.use_gtest
        cmake.definitions["FSEAM_BUILD_TESTS"] = False
        cmake.configure(
            source_folder=self._source_subfolder,
            build_folder=self._build_subfolder
        )
        return cmake

    def build(self):
        tools.patch(**self.conan_data["patches"][self.version])

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.builddirs = [os.path.join("lib", "cmake", self.project)]
        self.cpp_info.names["cmake_find_package"] = self.project
        self.cpp_info.names["cmake_find_package_multi"] = self.project
