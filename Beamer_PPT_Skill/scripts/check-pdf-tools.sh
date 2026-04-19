#!/bin/bash
# PDF Tool Detection Script for Beamer PPT Skill
# Checks for available PDF-to-image conversion tools

echo "=========================================="
echo "PDF-to-Image Tool Detection"
echo "=========================================="
echo ""

# Initialize status variables
PDFTOPPM_AVAILABLE=false
IMAGEMAGICK_AVAILABLE=false
PDF2IMAGE_AVAILABLE=false
POPPLER_AVAILABLE=false

# Check for pdftoppm (best option)
if command -v pdftoppm &> /dev/null; then
    PDFTOPPM_AVAILABLE=true
    PDFTOPPM_VERSION=$(pdftoppm -v 2>&1 | head -1)
    echo "✓ pdftoppm found (optimal)"
    echo "  Version: $PDFTOPPM_VERSION"
else
    echo "✗ pdftoppm not found"
    echo "  Install: macOS 'brew install poppler', Ubuntu 'sudo apt-get install poppler-utils'"
fi

echo ""

# Check for ImageMagick (fallback)
if command -v convert &> /dev/null; then
    # Verify it's ImageMagick, not other convert tool
    if convert --version 2>&1 | grep -q "ImageMagick"; then
        IMAGEMAGICK_AVAILABLE=true
        IMAGEMAGICK_VERSION=$(convert --version 2>&1 | head -1)
        echo "✓ ImageMagick found (fallback)"
        echo "  Version: $IMAGEMAGICK_VERSION"
    else
        echo "⚠ 'convert' command found but not ImageMagick"
    fi
else
    echo "✗ ImageMagick not found"
    echo "  Install: macOS 'brew install imagemagick', Ubuntu 'sudo apt-get install imagemagick'"
fi

echo ""

# Check for pdf2image Python package
if python3 -c "import pdf2image" 2>/dev/null; then
    PDF2IMAGE_AVAILABLE=true
    echo "✓ pdf2image (Python) found (alternative)"
    
    # Check if poppler is available for pdf2image
    if python3 -c "from pdf2image import convert_from_path; convert_from_path.__doc__" 2>/dev/null; then
        echo "  Note: pdf2image requires poppler utils to be installed"
    fi
else
    echo "✗ pdf2image (Python) not found"
    echo "  Install: 'pip install pdf2image' (also requires poppler)"
fi

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="

if [ "$PDFTOPPM_AVAILABLE" = true ]; then
    echo "✓ Visual mode: FULLY SUPPORTED"
    echo "  Recommended tool: pdftoppm (fastest, best quality)"
    echo "  Resolution: 150 DPI optimal"
elif [ "$IMAGEMAGICK_AVAILABLE" = true ]; then
    echo "⚠ Visual mode: LIMITED SUPPORT"
    echo "  Available: ImageMagick (slower, may have security policy issues)"
    echo "  Recommendation: Install pdftoppm for better experience"
elif [ "$PDF2IMAGE_AVAILABLE" = true ]; then
    echo "⚠ Visual mode: PYTHON REQUIRED"
    echo "  Available: pdf2image library"
    echo "  Note: Still requires poppler to be installed"
else
    echo "✗ Visual mode: NOT AVAILABLE"
    echo "  No PDF-to-image tools detected"
    echo "  Will use text-only mode for previews"
    echo ""
    echo "To enable visual mode, install one of:"
    echo "  1. poppler (recommended) - provides pdftoppm"
    echo "     macOS:   brew install poppler"
    echo "     Ubuntu:  sudo apt-get install poppler-utils"
    echo "     Windows: https://www.xpdfreader.com/download.html"
    echo ""
    echo "  2. ImageMagick (fallback)"
    echo "     macOS:   brew install imagemagick"
    echo "     Ubuntu:  sudo apt-get install imagemagick"
    echo ""
    echo "  3. pdf2image Python library + poppler"
    echo "     pip install pdf2image"
fi

echo ""
echo "=========================================="

# Return appropriate exit code for scripting
if [ "$PDFTOPPM_AVAILABLE" = true ] || [ "$IMAGEMAGICK_AVAILABLE" = true ] || [ "$PDF2IMAGE_AVAILABLE" = true ]; then
    exit 0
else
    exit 1
fi
