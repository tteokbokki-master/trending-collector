from datetime import datetime

DESCRIPTION_BLOCK = """# 🔥 GitHub Trending C/C++ 레포 수집

매일 오후 10시(KST), Github Trending에서 C 및 C++ 트렌딩 저장소를 자동으로 수집합니다.

---
"""

def count_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return sum(1 for line in f if line.strip())
    except FileNotFoundError:
        return 0

def prepend_result_block(result_block, readme_path="README.md"):
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    if not content.startswith("# 🔥 GitHub Trending"):
        new_content = DESCRIPTION_BLOCK + "\n" + result_block
    else:
        parts = content.split("---", 1)
        if len(parts) == 2:
            _, rest = parts
            new_content = DESCRIPTION_BLOCK + "\n" + result_block + rest
        else:
            new_content = DESCRIPTION_BLOCK + "\n" + result_block + "\n" + content

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    today = datetime.now().strftime("%y-%m-%d")
    c_added = count_lines("c_pending.txt")
    cpp_added = count_lines("cpp_pending.txt")
    c_done = count_lines("./done/c_done.txt")
    cpp_done = count_lines("./done/cpp_done.txt")

    result_block = f"""---

{today}

C 저장소 추가: {c_added}개  
C++ 저장소 추가: {cpp_added}개  

완료된 C 저장소: {c_done}개  
완료된 C++ 저장소: {cpp_done}개

"""
    prepend_result_block(result_block)

if __name__ == "__main__":
    main()