// hook-install.ts — pre-commit hook installer
// Usage: npx laon-vaultguard hook install [--force]

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const HOOK_NAME = 'pre-commit';

const HOOK_SCRIPT = `#!/bin/bash
# LAON VaultGuard pre-commit hook
# Scans staged files for secrets before commit.
# Bypass: git commit --no-verify

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)
if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

echo "🔍 LAON VaultGuard: scanning staged files..."
echo "$STAGED_FILES" | head -10
if [ $(echo "$STAGED_FILES" | wc -l) -gt 10 ]; then
  echo "  ... and $(($(echo "$STAGED_FILES" | wc -l) - 10)) more files"
fi

# temp list for quick regex scan
TMPDIR=$(mktemp -d)
echo "$STAGED_FILES" > "$TMPDIR/staged.txt"

# Run fast regex scan on staged content
FOUND=0
while IFS= read -r file; do
  [ -z "$file" ] && continue
  content=$(git show ":$file" 2>/dev/null)
  if [ -z "$content" ]; then continue; fi

  # Quick regex for critical patterns
  if echo "$content" | grep -qE '(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36,}|sk-[A-Za-z0-9]{32,}|-----BEGIN.*PRIVATE KEY-----|AIza[0-9A-Za-z_-]{35})'; then
    echo ""
    echo "⚠️  SECRET DETECTED in $file"
    echo "   Run: npx laon-vaultguard scan for detailed analysis"
    echo "   Bypass: git commit --no-verify"
    FOUND=1
  fi
done < "$TMPDIR/staged.txt"

rm -rf "$TMPDIR"

if [ $FOUND -eq 1 ]; then
  echo ""
  echo "🚫 Commit blocked by LAON VaultGuard."
  echo "   Review the warnings above or use --no-verify to bypass."
  exit 1
fi

echo "✅ No secrets detected in staged files."
exit 0
`;

export function installHook(repoPath: string, force = false): { installed: boolean; message: string } {
  const hooksDir = path.join(repoPath, '.git', 'hooks');

  if (!fs.existsSync(hooksDir)) {
    return { installed: false, message: `Not a git repository: ${repoPath}` };
  }

  const hookPath = path.join(hooksDir, HOOK_NAME);

  if (fs.existsSync(hookPath) && !force) {
    return {
      installed: false,
      message: `Hook already exists: ${hookPath}\n  Use --force to overwrite.`,
    };
  }

  fs.writeFileSync(hookPath, HOOK_SCRIPT, { mode: 0o755 });
  return { installed: true, message: `✅ Installed: ${hookPath}` };
}

export function uninstallHook(repoPath: string): { removed: boolean; message: string } {
  const hookPath = path.join(repoPath, '.git', 'hooks', HOOK_NAME);

  if (!fs.existsSync(hookPath)) {
    return { removed: false, message: `No hook found: ${hookPath}` };
  }

  const content = fs.readFileSync(hookPath, 'utf-8');
  if (!content.includes('LAON VaultGuard')) {
    return { removed: false, message: `Hook exists but was not installed by LAON VaultGuard. Manual removal required: ${hookPath}` };
  }

  fs.unlinkSync(hookPath);
  return { removed: true, message: `✅ Removed: ${hookPath}` };
}

// ── CLI entry ──

export function hookCli(args: string[]) {
  const command = args[0];
  const repoPath = args.find(a => !a.startsWith('-') && a !== command) || process.cwd();

  if (command === 'install') {
    const force = args.includes('--force') || args.includes('-f');
    const result = installHook(repoPath, force);
    console.log(result.message);
    process.exit(result.installed ? 0 : 1);
  }

  if (command === 'uninstall') {
    const result = uninstallHook(repoPath);
    console.log(result.message);
    process.exit(result.removed ? 0 : 1);
  }

  console.log('Usage: npx laon-vaultguard hook <install|uninstall> [path] [--force]');
  process.exit(1);
}
