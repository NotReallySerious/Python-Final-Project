import os
import subprocess
from datetime import datetime

'''
Use this script to update the repo guyss. just run it anywaym, no need to understand them now.
'''
FOLDERS = [
    "admin",
    "doctor",
    "accountant",
    "cashier",
    "login",
    "pharmacist"
]

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def main():
    username = input("Enter your username (for commit message): ").strip()
    if not username:
        print("Username is required")
        return

    print("\nAvailable folders:")
    for i, f in enumerate(FOLDERS, 1):
        print(f"{i}. {f}")

    choice = input("\nSelect folder number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(FOLDERS)):
        print("Invalid choice")
        return

    folder = FOLDERS[int(choice) - 1]
    os.makedirs(folder, exist_ok=True)

    filename = input("Enter python filename (without .py): ").strip()
    if not filename:
        print("Filename required")
        return

    filepath = os.path.join(folder, filename + ".py")

    print("\nEnter your Python code")
    print("(CTRL+D on Linux/macOS | CTRL+Z then Enter on Windows)\n")

    code = ""
    try:
        while True:
            line = input()
            code += line + "\n"
    except EOFError:
        pass

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    run(f'git add "{filepath}"')

    commit_msg = (
        f"Add {filename}.py to {folder} - {username} "
        f"({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
    )

    run(f'git commit -m "{commit_msg}"')
    run("git push -u origin main")

    print("\n✅ Commit pushed successfully")
    print(f"📝 Commit message: {commit_msg}")

if __name__ == "__main__":
    main()
