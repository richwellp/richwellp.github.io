# Documentation

This folder contains comprehensive documentation for all major features implemented in the portfolio website.

## Available Documentation

### Command Palette Search
- **COMMAND_PALETTE_README.md** - Complete feature overview and usage guide
- **QUICK_REFERENCE.md** - Quick reference for using the command palette
- **TESTING_GUIDE.md** - Comprehensive testing procedures and test cases
- **DEPLOYMENT_CHECKLIST.md** - Pre-deployment checklist

### Image Optimization
- **IMAGE_OPTIMIZATION_REPORT.md** - Detailed technical report on WebP conversion
- **OPTIMIZATION_SUMMARY.md** - Quick summary of optimization results
- **OPTIMIZATION_COMPLETE.txt** - Completion summary with metrics

### Structured Data (SEO)
- **STRUCTURED_DATA_README.md** - Complete overview of Schema.org implementation
- **QUICK_START_STRUCTURED_DATA.md** - Fast reference for developers
- **STRUCTURED_DATA_GUIDE.md** - Comprehensive guide with examples
- **STRUCTURED_DATA_SUMMARY.md** - Technical summary
- **STRUCTURED_DATA_TESTING.md** - Testing and validation guide
- **STRUCTURED_DATA_DELIVERY.md** - Delivery and deployment summary

### Implementation Details
- **IMPLEMENTATION_COMPLETE.md** - Overall implementation summary
- **IMPLEMENTATION_SUMMARY.md** - Technical implementation details
- **FILES_CHANGED.md** - Complete listing of modified files

## Quick Links

### For Users
- Press **Cmd/Ctrl + K** to open command palette search
- Reading time and table of contents automatically appear on blog posts
- Theme toggles between Light, Auto (system), and Dark modes

### For Developers
- Run `npm run optimize:images` to convert images to WebP
- Check STRUCTURED_DATA_TESTING.md for SEO validation steps
- Review TESTING_GUIDE.md for comprehensive test cases

## Project Structure

```
frontend/
├── docs/                    # This documentation folder
├── public/                  # Static assets
│   ├── assets/photos/      # Optimized images (WebP + originals)
│   └── blog/               # Blog post markdown files
├── scripts/                # Build scripts
│   └── optimize-images.js  # Image optimization script
├── src/
│   ├── components/         # Vue components
│   │   ├── CommandPalette.vue
│   │   ├── OptimizedImage.vue
│   │   └── TableOfContents.vue
│   ├── composables/        # Vue composables
│   │   ├── useStructuredData.js
│   │   ├── useTheme.js (enhanced with auto mode)
│   │   └── useBlog.js (reading time + headings)
│   └── views/              # Page components
└── package.json            # Dependencies (fuse.js, sharp)
```

## Recent Major Updates

### February 23, 2026
- ✅ Command palette search with Cmd/Ctrl+K
- ✅ WebP image optimization (55% size reduction)
- ✅ Blog reading time + table of contents
- ✅ Schema.org structured data for SEO
- ✅ System preference detection for theme (Auto mode)

## Getting Help

For questions or issues:
1. Check the relevant documentation file above
2. Review the implementation summaries
3. Check git commit history for context
4. Refer to inline code comments in source files

---

**Last Updated:** February 23, 2026
