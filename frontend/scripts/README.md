# Image Optimization Scripts

## Overview
This directory contains scripts for optimizing portfolio images for web performance.

## Scripts

### optimize-images.js
Converts all JPEG/PNG images in `/public/assets/photos/` to WebP format with multiple size variants.

**Usage:**
```bash
npm run optimize:images
```

**What it does:**
1. Scans `/public/assets/photos/` recursively for JPEG/PNG files
2. Generates 3 WebP variants for each image:
   - **Thumbnail** (400px width): `filename_thumb.webp`
   - **Medium** (800px width): `filename_md.webp`
   - **Full** (1920px width): `filename.webp`
3. Applies 75% quality compression
4. Maintains aspect ratios
5. Keeps original files as fallbacks

**Output Example:**
```
Processing: /assets/photos/travel/japan/20240603_194332.jpg
  ✓ Created thumbnail: /travel/japan/20240603_194332_thumb.webp (45.35 KB)
  ✓ Created medium: /travel/japan/20240603_194332_md.webp (145.75 KB)
  ✓ Created full: /travel/japan/20240603_194332.webp (382.95 KB)

=============================================
  Optimization Complete!
=============================================
Images processed: 13
WebP files created: 39
Total saved: 12.6 MB
Reduction: 55%
```

## Configuration

### Adjusting Quality
Edit `optimize-images.js` line 12:
```javascript
const QUALITY = 75 // Change to 60-90 range
```

### Modifying Sizes
Edit `optimize-images.js` lines 13-17:
```javascript
const SIZES = {
  thumbnail: { width: 400, suffix: '_thumb' },
  medium: { width: 800, suffix: '_md' },
  full: { width: 1920, suffix: '' }
}
```

## When to Run

Run the optimization script when:
- Adding new images to `/public/assets/photos/`
- Updating existing images
- Changing quality/size settings
- After cloning the repository (if WebP files aren't committed)

## Requirements

- Node.js 20+ or 22+
- sharp package (installed as devDependency)

## Troubleshooting

### Script fails with "sharp" error
```bash
npm install --save-dev sharp
```

### Images not found
Ensure images are in `/public/assets/photos/` directory with supported extensions (.jpg, .jpeg, .png)

### WebP files too large/small
Adjust the `QUALITY` constant (higher = larger files, better quality)

## Integration with Components

The generated WebP files are automatically used by the `OptimizedImage` component:

```vue
<OptimizedImage
  src="/assets/photos/travel/photo.jpg"
  size="md"
  alt="Description"
/>
```

This will load `photo_md.webp` with automatic fallback to `photo.jpg` in unsupported browsers.
