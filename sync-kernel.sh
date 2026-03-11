#!/bin/bash
# sync-kernel.sh — Syncs the System Kernel and Framework to all AI tool formats
# Run this whenever agent.md or guide files are updated.
# Usage: ./scripts/sync-kernel.sh
#
# What it does:
#   1. Copies agent.md to tool-specific rule files (Cursor, Claude Code, Windsurf)
#   2. Sets up Antigravity's .agents/ folder with workflows and skills
#   3. Verifies all files are in sync

set -e

KERNEL="agent.md"
GUIDES_DIR="docs/guides"
SKILLS_DIR="skills"

# Tool-specific rule files (Cursor, Claude Code, Windsurf)
TOOL_TARGETS=(".cursorrules" "CLAUDE.md" ".windsurfrules")

# Antigravity paths
AGY_ROOT=".agents"
AGY_WORKFLOWS="$AGY_ROOT/workflows"
AGY_SKILLS="$AGY_ROOT/skills"

echo "🔄 AI Agent Framework — Kernel Sync"
echo "====================================="
echo ""

# ─────────────────────────────────────────────────
# STEP 1: Sync kernel to tool-specific rule files
# ─────────────────────────────────────────────────
if [ ! -f "$KERNEL" ]; then
    echo "❌ Error: $KERNEL not found in project root."
    echo "   Run this script from the project root directory."
    exit 1
fi

echo "📋 Step 1: Syncing kernel to tool-specific files..."
for target in "${TOOL_TARGETS[@]}"; do
    cp "$KERNEL" "$target"
    echo "   ✅ $target"
done
echo ""

# ─────────────────────────────────────────────────
# STEP 2: Set up Antigravity .agents/ structure
# ─────────────────────────────────────────────────
echo "🚀 Step 2: Setting up Antigravity .agents/ structure..."

# Create directories
mkdir -p "$AGY_WORKFLOWS"
mkdir -p "$AGY_SKILLS"

# Copy kernel as a workflow (always available to Antigravity)
cp "$KERNEL" "$AGY_WORKFLOWS/agent-kernel.md"
echo "   ✅ $AGY_WORKFLOWS/agent-kernel.md (kernel)"

# Copy guide files to workflows
if [ -d "$GUIDES_DIR" ]; then
    for guide in "$GUIDES_DIR"/*.md; do
        if [ -f "$guide" ]; then
            filename=$(basename "$guide")
            cp "$guide" "$AGY_WORKFLOWS/$filename"
            echo "   ✅ $AGY_WORKFLOWS/$filename"
        fi
    done
else
    echo "   ⚠️  $GUIDES_DIR not found — skipping guide sync."
    echo "      Create $GUIDES_DIR and place your 00-09 guide files there."
fi

# Copy AgentSpec.md if it exists
if [ -f "docs/AgentSpec.md" ]; then
    cp "docs/AgentSpec.md" "$AGY_WORKFLOWS/AgentSpec.md"
    echo "   ✅ $AGY_WORKFLOWS/AgentSpec.md (what to build)"
elif [ -f "AgentSpec.md" ]; then
    cp "AgentSpec.md" "$AGY_WORKFLOWS/AgentSpec.md"
    echo "   ✅ $AGY_WORKFLOWS/AgentSpec.md (what to build)"
else
    echo "   ⚠️  AgentSpec.md not found — skipping."
    echo "      Generate it using MASTER_AGENT_DISCOVERY_PROMPT.md"
fi

# Copy skills to .agents/skills/ (each skill is its own folder)
if [ -d "$SKILLS_DIR" ]; then
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            mkdir -p "$AGY_SKILLS/$skill_name"
            cp -r "$skill_dir"* "$AGY_SKILLS/$skill_name/"
            echo "   ✅ $AGY_SKILLS/$skill_name/"
        fi
    done
else
    echo "   ⚠️  $SKILLS_DIR not found — skipping skill sync."
    echo "      Skills will be created via /new-skill command."
fi

echo ""

# ─────────────────────────────────────────────────
# STEP 3: Verify
# ─────────────────────────────────────────────────
echo "📊 Step 3: Verification"
echo "   Tool files:"
for target in "${TOOL_TARGETS[@]}"; do
    if [ -f "$target" ]; then
        echo "      ✅ $target ($(wc -c < "$target") bytes)"
    else
        echo "      ❌ $target MISSING"
    fi
done

echo "   Antigravity:"
if [ -d "$AGY_WORKFLOWS" ]; then
    wf_count=$(find "$AGY_WORKFLOWS" -name "*.md" | wc -l)
    echo "      ✅ $AGY_WORKFLOWS/ ($wf_count workflows)"
fi
if [ -d "$AGY_SKILLS" ]; then
    sk_count=$(find "$AGY_SKILLS" -mindepth 1 -maxdepth 1 -type d | wc -l)
    echo "      ✅ $AGY_SKILLS/ ($sk_count skills)"
fi

echo ""
echo "====================================="
echo "✅ Sync complete."
echo ""
echo "📌 Reminders:"
echo "   • For Gemini Custom Instructions: manually paste agent.md content"
echo "   • Commit all synced files together"
echo "   • Notify the team of any kernel changes"
