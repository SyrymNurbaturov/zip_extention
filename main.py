import os, io
import zipfile
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

allowed_extensions = {'.zip', '.rar', '.tar', '.gzip', '.7z', '.bz2', '.xz', '.z', '.tar.gz', '.tar.bz2', '.tar.xz', '.tar.z',
                      '.tgz', '.tbz2', '.txz', '.cab', '.iso', '.jar', '.lz', '.lzma', '.lzo', '.rpm', '.deb', '.zoo', '.zpaq', '.arc', '.wim', '.arj', '.a', '.bz', '.bzip2',
                      '.gz', '.gzip', '.lz4', '.lzop', '.sz', '.tlz', '.zst'}

def check_zip_contents(zip_file_path):
    found_extensions = set()

    def recursive_check(zip_file):
        for file_info in zip_file.infolist():
            if file_info.is_dir():
                continue
            found_extension = os.path.splitext(file_info.filename)[1]
            found_extensions.add(found_extension.lower())
            if file_info.filename.endswith('.zip'):
                nested_zip_path = file_info.filename
                with zip_file.open(nested_zip_path) as nested_zip_bytes:
                    nested_zip_data = io.BytesIO(nested_zip_bytes.read())
                with zipfile.ZipFile(nested_zip_data, 'r') as nested_zip_file:
                    recursive_check(nested_zip_file)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        recursive_check(zip_file)

    return found_extensions

@app.post('/check_zip')
def check_zip(zip_file: UploadFile = File(...)):
    temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    temp_zip.close()

    try:
        with open(temp_zip.name, 'wb') as f:
            f.write(zip_file.file.read())

        file_ext = os.path.splitext(temp_zip.name)[1].lower()
        if file_ext not in allowed_extensions:
            return JSONResponse(content={"error": "Invalid file format. Allowed formats: .zip, .rar and etc."}, status_code=400)

        found_extensions = check_zip_contents(temp_zip.name)
        os.remove(temp_zip.name)

        if not found_extensions:
            return JSONResponse(content={"error": "No supported files found in the ZIP."}, status_code=400)

        found_languages = [language_dict[ext] for ext in found_extensions if ext in language_dict]

        found_configurations = [config_dict[ext] for ext in found_extensions if ext in config_dict]

        other_extensions = [ext for ext in found_extensions if ext not in language_dict and ext not in config_dict]

        return {'found_languages': found_languages, 'found_configurations': found_configurations, 'other_extensions':other_extensions}

    except Exception as e:
        print("Exception:", str(e))

        return JSONResponse(content={"error": "An error occurred while processing the file. Details: " + str(e)}, status_code=500)
language_dict = {
    '.php': 'PHP',
    '.py': 'Python',
    '.cpp': 'C++',
    '.js': 'JavaScript',
    '.java': 'Java',
    '.rb': 'Ruby',
    '.ts': 'TypeScript',
    '.swift': 'Swift',
    '.go': 'Go',
    '.c': 'C',
    '.cs': 'C#',
    '.lua': 'Lua',
    '.pl': 'Perl',
    '.scala': 'Scala',
    '.r': 'R',
    '.jsx': 'React',
    '.html': 'HTML',
    '.css': 'CSS',
    '.sql': 'SQL',
    '.vb': 'Visual Basic',
    '.asm': 'Assembly',
    '.kt': 'Kotlin',
    '.h': 'C/C++ Header',
    '.scss': 'Sass',
    '.less': 'Less',
    '.rs': 'Rust',
    '.ejs': 'Embedded JavaScript',
    '.bash': 'Bash',
    '.jsp': 'Java Server Pages',
    '.asp': 'ASP.NET',
    '.tsx': 'React TypeScript',
    '.coffee': 'CoffeeScript',
    '.dart': 'Dart',
    '.jl': 'Julia',
    '.ps1': 'PowerShell',
    '.bat': 'Batch Script',
    '.m': 'MATLAB',
    '.groovy': 'Groovy',
    '.elm': 'Elm',
    '.vue': 'Vue.js',
    '.tcl': 'Tcl',
    '.vhdl': 'VHDL',
    '.cob': 'COBOL',
    '.ml': 'OCaml',
    '.erl': 'Erlang',
    '.d': 'D',
    '.lisp': 'Lisp',
    '.wasm': 'WebAssembly',
    '.v': 'Verilog',
    '.ada': 'Ada',
    '.f95': 'Fortran',
    '.styl': 'Stylus',
    '.slim': 'Slim',
    '.hbs': 'Handlebars',
    '.thrift': 'Thrift',
    '.pig': 'Pig',
    '.nim': 'Nim',
    '.zig': 'Zig',
    '.zsh': 'Zsh',
    '.fish': 'Fish',
    '.nix': 'Nix',
    '.awk': 'Awk',
    '.bc': 'BC',
    '.cbl': 'COBOL',
    '.cfm': 'ColdFusion',
    '.clj': 'Clojure',
    '.ex': 'Elixir',
    '.factor': 'Factor',
    '.forth': 'Forth',
    '.fr': 'Forth',
    '.litcoffee': 'CoffeeScript',
    '.nsi': 'NSIS',
    '.nse': 'NuSMV',
    '.ooc': 'OOC',
    '.pike': 'Pike',
    '.pl6': 'Perl 6',
    '.pm6': 'Perl 6',
    '.prg': 'xBase',
    '.proto': 'Protocol Buffers',
    '.pwn': 'Pawn',
    '.sc': 'SuperCollider',
    '.sl': 'ShaderLab',
    '.sty': 'TeX',
    '.tex': 'TeX',
    '.w': 'Wolfram Language',
    '.y': 'Yacc',
    '.blade.html': 'Blade HTML (Laravel)',
}

config_dict = {
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.ini': 'INI',
    '.xml': 'XML',
    '.properties': 'Properties',
    '.toml': 'TOML',
    '.env': 'Environment Variable',
    '.sh': 'Shell Script',
    '.bash': 'Bash Script',
    '.ps1': 'PowerShell Script',
    '.cfg': 'Configuration',
    '.conf': 'Configuration',
    '.cnf': 'Configuration',
    '.htaccess': 'htaccess',
    '.nginx': 'Nginx Configuration',
    '.htpasswd': 'htpasswd',
    '.dockerfile': 'Dockerfile',
    '.compose': 'Docker Compose',
    '.gitignore': 'Git Ignore',
    '.gitconfig': 'Git Configuration',
    '.npmrc': 'npm Configuration',
    '.yarnrc': 'Yarn Configuration',
    '.gradle': 'Gradle Configuration',
    '.maven': 'Maven Configuration',
    '.editorconfig': 'EditorConfig',
    '.stylelintrc': 'Stylelint Configuration',
    '.eslint': 'ESLint Configuration',
    '.prettierrc': 'Prettier Configuration',
    '.babelrc': 'Babel Configuration',
    '.webpack': 'Webpack Configuration',
    '.tsconfig': 'TypeScript Configuration',
    '.php': 'PHP Configuration',
    '.sql': 'SQL Configuration',
    '.jar': 'Java Archive',
    '.war': 'Web Archive',
    '.ear': 'Enterprise Archive',
}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

