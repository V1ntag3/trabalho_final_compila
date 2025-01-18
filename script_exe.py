import subprocess
import os

def compile_assembly(assembly_file, output_file):
    print(f"Compiling assembly code from {assembly_file}...")
    compile_command = ["nasm", "-f", "macho64", assembly_file, "-o", output_file + ".o"]
    subprocess.run(compile_command, check=True)

def link_object_to_executable(object_file, executable_file):
    print(f"Linking object file {object_file} to executable {executable_file}...")
    link_command = ["clang", "-arch", "arm64", "-o", executable_file, object_file]
    subprocess.run(link_command, check=True)

def make_executable(executable_file):
    print(f"Making {executable_file} executable...")
    os.chmod(executable_file, 0o755)

def run_executable(executable_file):
    print(f"Running the executable {executable_file}...")
    subprocess.run(["./" + executable_file], check=True)

def main():
    assembly_file = "assembly_code.s"  
    object_file = "assembly_code"      
    executable_file = "program"       

    try:
        compile_assembly(assembly_file, object_file)
        link_object_to_executable(object_file + ".o", executable_file)
        make_executable(executable_file)
        run_executable(executable_file)

    except subprocess.CalledProcessError as e:
        print(f"Erro durante o processo: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
