from abc import ABCMeta, abstractmethod


class Compiler(metaclass=ABCMeta):
    @abstractmethod
    def collect_source(self):
        pass

    @abstractmethod
    def compile_to_object(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def compile_and_run(self):
        self.collect_source()
        self.compile_to_object()
        self.run()


class iOSCompiler(Compiler):
    def collect_source(self):
        print("Collect Swift source")

    def compile_to_object(self):
        print("Compile code to bitcode")

    def run(self):
        print("Run program")


compiler = iOSCompiler()
compiler.compile_and_run()