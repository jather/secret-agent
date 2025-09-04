from functions.get_files_info import get_files_info

get_files_info("calculator", ".")
get_files_info("calculator", "pkg")

try:
    get_files_info("calculator", "/bin")
except Exception as e:
    print(e)

try:
    get_files_info("calculator", "../")
except Exception as e:
    print(e)
