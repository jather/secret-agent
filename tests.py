from functions.get_files_content import get_files_content

print(get_files_content("calculator", "main.py"))
print(get_files_content("calculator", "pkg/calculator.py"))
try:
    print(get_files_content("calculator", "/bin/cat"))
except Exception as e:
    print(e)

try:
    print(get_files_content("calculator", "pkg/does_not_exist.py"))
except Exception as e:
    print(e)
