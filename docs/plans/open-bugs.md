# Open Bugs

No open bugs currently tracked.

## Recently Resolved

Latest fixes (2026-05-18):

1. **VS Code DevContainer permission denied** - Fixed /sandbox directory ownership

   - Resolution: Added chown for /sandbox directory in Dockerfile after UID changes. Previous fix only handled /home/sandbox and /home/ubuntu, but sandbox user's HOME is /sandbox.
   - Commit: harness-sandbox (modified Dockerfile)
   - Validation: ✅ /sandbox owned by sandbox:1000, VS Code can create .vscode-server directory
   - Story points: 1

Previous fixes (2026-05-17):

2. **Claude Code configuration in Sandbox** - Fixed credential file access

   - Spec: [docs/specs/bug-fix-claude-config-in-sandbox.md](../specs/bug-fix-claude-config-in-sandbox.md)
   - Resolution: Modified Dockerfile to change sandbox user UID from 998→1000, matching host user for credential file access (mode 600)
   - Commit: harness-sandbox (modified Dockerfile, docker-compose.yml, .env.example)
   - Validation: ✅ Config file readable, Claude Code operational (v2.1.91), no permission errors
   - Story points: 2

3. **Missing deepwiki/litho skills** - Integrated 3 skills via RPC model

   - Spec: [docs/specs/bug-fix-missing-deepwiki-skills.md](../specs/bug-fix-missing-deepwiki-skills.md)
   - Resolution: Fixed plugin manifest, created wrapper skills using docker exec to litho container (Model B - RPC approach, +0 MB vs +1.24 GB for Rust toolchain)
   - Commit: harness-tooling bf7c5ff (plugin.json, 3 skill files)
   - Validation: ✅ Plugin manifest valid, skills exist with correct frontmatter, litho container operational
   - Story points: 3

4. **Litho CA certificate configuration** - Fixed HTTPS connectivity for corporate proxy

   - Spec: [docs/specs/fix-litho-ca-certificate.md](../specs/fix-litho-ca-certificate.md)
   - Resolution: Added explicit SSL environment variables to docker-compose.yml litho service
   - Commit: harness-sandbox c5b60bd
   - Validation: ✅ HTTPS connectivity works, litho runs without CA errors
   - Story points: 1

Previous fixes merged to `dev` branch:

5. **Litho container read-only mount failure** - Fixed nested mount conflict on harness up

   - Spec: [docs/specs/bug-fix-litho-readonly-mount.md](../specs/bug-fix-litho-readonly-mount.md)
   - Resolution: Moved litho cache to `/litho-cache` (sibling path), removed hardcoded `PROJECT_NAME`, added cache pre-creation
   - Story points: 3
6. **Invalid Char in .harness.yml** - Fixed em-dash characters in template

   - Spec: [docs/specs/bug-fix-invalid-char-harness-yml.md](../specs/bug-fix-invalid-char-harness-yml.md)
   - Resolution: Replaced 28 em-dash chars with ASCII hyphens
   - Story points: 1
7. **Default to stony compose profile** - Unified corporate/private build system

   - Spec: [docs/specs/bug-fix-stony-compose-profile.md](../specs/bug-fix-stony-compose-profile.md)
   - Resolution: Added `harness build --corporate/--private`, consolidated .env, deleted deprecated files
   - Story points: 13
8. **Wrong agent yml files** - Template shipped with .yml instead of .md

   - Spec: [docs/specs/bug-fix-wrong-agent-format.md](../specs/bug-fix-wrong-agent-format.md)
   - Resolution: Removed .yml files, added pre-commit hook, documented .md requirement
   - Story points: 2
9. **Claude startup errors** - Plugin path mismatch for all-my-skills

   - Spec: [docs/specs/bug-fix-claude-startup-errors.md](../specs/bug-fix-claude-startup-errors.md)
   - Resolution: Created .claude-plugin/plugin.json, fixed marketplace.json source path
   - Story points: 2

All fixes merged and pushed to origin/dev on 2026-05-14.
