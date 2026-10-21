import os
import sys
import json
import re
import shutil
import subprocess
from pathlib import Path

LOCAL_SKILL = Path(r"C:\Users\bedly\.codex\skills\ultimate-frontend-designer")
REPO_DIR = Path(r"C:\Users\bedly\Documents\Codex\2026-10-13\github-skill-ultimate-frontend-designer-c\work\repo")

def run():
    if not LOCAL_SKILL.exists():
        print(f"Error: Local skill not found at {LOCAL_SKILL}")
        return 1
    if not REPO_DIR.exists():
        print(f"Error: Repo not found at {REPO_DIR}")
        return 1

    repo_skill = REPO_DIR / "skills" / "ultimate-frontend-designer"
    
    # Copy & sanitize files
    for src in LOCAL_SKILL.rglob("*"):
        if src.is_file():
            rel = src.relative_to(LOCAL_SKILL)
            dest = repo_skill / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.suffix == ".md":
                txt = src.read_text(encoding="utf-8")
                txt = re.sub(r'\[\$imagegen\]\([A-Za-z]:[\\/]Users[\\/][^\s\)\]\"\'`]+imagegen/SKILL\.md\)', 'imagegen', txt)
                txt = re.sub(r'\[\$gpt-image\]\([A-Za-z]:[\\/]Users[\\/][^\s\)\]\"\'`]+gpt-image/SKILL\.md\)', 'gpt-image', txt)
                txt = re.sub(r'[A-Za-z]:[\\/]Users[\\/][^\s\)\]\"\'`]+react-bits', 'react-bits', txt)
                txt = re.sub(r'node \"[A-Za-z]:[\\/]Users[\\/][^\s\)\]\"\'`]+duo-dev/dist/index\.js\"', 'duo-dev', txt)
                txt = txt.replace("→ prebuild_review(Design Gate) → implementation(通过 duo-dev 自动工程化) → verification(Build Gate) → delivery",
                                  "→ prebuild_review → implementation → verification → delivery")
                dest.write_text(txt, encoding="utf-8")
            else:
                shutil.copy2(src, dest)

    # Sync version to manifests
    main_txt = (repo_skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'version: \"([^\"]+)\"', main_txt)
    if not m:
        print("Error: version not found in SKILL.md")
        return 1
    ver = m.group(1)

    for p in [REPO_DIR / "plugin.json", REPO_DIR / ".codex-plugin" / "plugin.json", REPO_DIR / ".claude-plugin" / "plugin.json", REPO_DIR / ".claude-plugin" / "marketplace.json"]:
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8-sig"))
            if "version" in data:
                data["version"] = ver
            if "plugins" in data and isinstance(data["plugins"], list):
                for item in data["plugins"]:
                    if isinstance(item, dict) and "version" in item:
                        item["version"] = ver
            p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Run validation
    val_script = REPO_DIR / "scripts" / "validate.py"
    res = subprocess.run([sys.executable, "-X", "utf8", str(val_script)], capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        print("Validation failed:")
        print(res.stderr or res.stdout)
        return 1

    # Check git status
    st = subprocess.run(["git", "-C", str(REPO_DIR), "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8")
    if not st.stdout.strip():
        print(f"Everything is up to date (version {ver}). No uncommitted changes.")
        return 0

    # Commit and push
    subprocess.run(["git", "-C", str(REPO_DIR), "add", "-A"], check=True)
    msg = f"Update skill to v{ver}"
    subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", msg], check=True)
    push = subprocess.run(["git", "-C", str(REPO_DIR), "push", "origin", "main"], capture_output=True, text=True, encoding="utf-8")
    if push.returncode == 0:
        print(f"Successfully synced and pushed v{ver} to GitHub!")
        return 0
    else:
        print("Push error:", push.stderr or push.stdout)
        return 1

if __name__ == "__main__":
    sys.exit(run())

