from functions.get_files_info import get_files_info

tests = [".", "pkg", "/bin", "../"]

for test in tests:
    if test == ".":
        print(f"Result for current directory:")
        print(get_files_info("calculator", test))
        continue
    print(f"Result for {test} directory:")
    print(get_files_info("calculator", test))
