#!/bin/bash
# Build script for packaging the Blender WebStats addon

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_ROOT/build"
ADDON_NAME="blender-webstats"

# Clean and create build directory
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/$ADDON_NAME"

# Copy addon files to build directory
echo "Copying addon files..."
cp -r "$PROJECT_ROOT/src/blender_webstats" "$BUILD_DIR/$ADDON_NAME/"
cp "$PROJECT_ROOT/LICENSE" "$BUILD_DIR/$ADDON_NAME/"
cp "$PROJECT_ROOT/README.md" "$BUILD_DIR/$ADDON_NAME/"

# Copy root __init__.py that re-exports from src/blender_webstats
cp "$PROJECT_ROOT/__init__.py" "$BUILD_DIR/$ADDON_NAME/"

# Create the src directory structure in build
mkdir -p "$BUILD_DIR/$ADDON_NAME/src"
# The __init__.py imports from .src.blender_webstats, so we need this structure
cp -r "$PROJECT_ROOT/src/blender_webstats" "$BUILD_DIR/$ADDON_NAME/src/"

# Create zip file
cd "$BUILD_DIR"
ZIP_NAME="$ADDON_NAME.zip"
echo "Creating $ZIP_NAME..."
zip -r "$ZIP_NAME" "$ADDON_NAME"

echo "Build complete: $BUILD_DIR/$ZIP_NAME"
echo ""
echo "To install in Blender:"
echo "1. Open Blender"
echo "2. Go to Edit > Preferences > Add-ons"
echo "3. Click 'Install...' and select: $BUILD_DIR/$ZIP_NAME"
echo "4. Enable the 'Render: Blender WebStats' addon"
