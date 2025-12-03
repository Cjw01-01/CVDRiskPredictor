#!/usr/bin/env python3
"""
Script to remove Hugging Face token from git history
"""
import subprocess
import sys
import os
import json
import tempfile

def run_command(cmd, check=True, show_output=True):
    """Run a shell command and return output"""
    if show_output:
        print(f"Running: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    # Fill in your OLD token string here before running, e.g. "hf_xxx..."
    token = "PASTE_OLD_HF_TOKEN_HERE"
    replacement = "YOUR_HUGGINGFACE_TOKEN_HERE"
    
    print("=" * 60)
    print("Removing Hugging Face Token from Git History")
    print("=" * 60)
    print()
    
    # Check if git-filter-repo is available
    result = subprocess.run(
        "git filter-repo --version",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✓ git-filter-repo found - using it")
        use_filter_repo = True
    else:
        print("✗ git-filter-repo not found - will use git filter-branch")
        use_filter_repo = False
    
    # Create backup branch
    print("\n1. Creating backup branch...")
    backup_name = f"backup-before-token-cleanup-{subprocess.run('powershell -Command Get-Date -Format yyyyMMdd-HHmmss', shell=True, capture_output=True, text=True).stdout.strip()}"
    run_command(f"git branch {backup_name}", check=False)
    print(f"   Backup created: {backup_name}")
    
    if use_filter_repo:
        # Use git-filter-repo
        print("\n2. Using git-filter-repo to rewrite history...")
        replacements_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        replacements_file.write(f"{token}==>{replacement}\n")
        replacements_file.close()
        
        try:
            run_command(f'git filter-repo --replace-text "{replacements_file.name}" --force')
            print("✓ History rewritten successfully!")
        finally:
            os.unlink(replacements_file.name)
    else:
        # Use git filter-branch
        print("\n2. Using git filter-branch to rewrite history...")
        print("   This may take a while...")
        
        # Create a PowerShell script in the project directory (not temp, so it persists)
        ps_script_path = os.path.join(os.getcwd(), "temp_replace_token.ps1")
        with open(ps_script_path, 'w', encoding='utf-8') as f:
            f.write(f"""if (Test-Path 'notebooks/deep_fusion_notskewed.ipynb') {{
    $content = Get-Content 'notebooks/deep_fusion_notskewed.ipynb' -Raw -Encoding UTF8
    $content = $content -replace '{token}', '{replacement}'
    Set-Content 'notebooks/deep_fusion_notskewed.ipynb' -Value $content -NoNewline -Encoding UTF8
}}
""")
        
        try:
            # Set non-interactive editor environment variables
            env = os.environ.copy()
            env['GIT_EDITOR'] = 'echo'
            env['GIT_SEQUENCE_EDITOR'] = 'echo'
            env['EDITOR'] = 'echo'
            env['FILTER_BRANCH_SQUELCH_WARNING'] = '1'  # Suppress the warning
            
            # Configure git to use non-interactive editor
            subprocess.run("git config core.editor echo", shell=True, capture_output=True)
            subprocess.run("git config sequence.editor echo", shell=True, capture_output=True)
            
            # Use inline PowerShell command instead of file (more reliable)
            # Escape the quotes properly for the command
            ps_inline = f"powershell -Command \"if (Test-Path 'notebooks/deep_fusion_notskewed.ipynb') {{ $content = Get-Content 'notebooks/deep_fusion_notskewed.ipynb' -Raw -Encoding UTF8; $content = $content -replace '{token}', '{replacement}'; Set-Content 'notebooks/deep_fusion_notskewed.ipynb' -Value $content -NoNewline -Encoding UTF8 }}\""
            cmd = f'git filter-branch -f --tree-filter "{ps_inline}" -- --all'
            
            print(f"   Executing filter-branch (this may take a moment)...")
            print(f"   Using script: {ps_script_windows}")
            result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print("✓ History rewritten successfully!")
                # Clean up refs
                print("   Cleaning up backup refs...")
                subprocess.run("git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin", shell=True, capture_output=True)
                subprocess.run("git reflog expire --expire=now --all", shell=True, capture_output=True)
                subprocess.run("git gc --prune=now --aggressive", shell=True, capture_output=True)
            else:
                print(f"✗ Error occurred:")
                if result.stderr:
                    print(result.stderr)
                if result.stdout:
                    print(result.stdout)
                print(f"\nScript location: {ps_script_windows}")
                print("You can manually run the PowerShell script to verify it works.")
                sys.exit(1)
        finally:
            # Clean up the script file
            try:
                if os.path.exists(ps_script_path):
                    os.unlink(ps_script_path)
            except:
                pass
    
    print("\n" + "=" * 60)
    print("History cleanup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Verify token string is removed:")
    print('   git log --all --full-history -- notebooks/deep_fusion_notskewed.ipynb | Select-String "YOUR_HF_TOKEN_HERE"')
    print("\n2. Push to GitHub:")
    print("   git push origin main --force")
    print("\n3. Revoke the old token at:")
    print("   https://huggingface.co/settings/tokens")
    print()

if __name__ == "__main__":
    main()

