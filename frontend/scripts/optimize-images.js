import { readdir, mkdir, stat } from 'fs/promises'
import { existsSync } from 'fs'
import { join, dirname, extname, basename } from 'path'
import { fileURLToPath } from 'url'
import sharp from 'sharp'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const PHOTOS_DIR = join(__dirname, '../public/assets/photos')
const SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png']
const QUALITY = 75 // 75% quality for good balance
const SIZES = {
  thumbnail: { width: 400, suffix: '_thumb' },
  medium: { width: 800, suffix: '_md' },
  full: { width: 1920, suffix: '' } // Full size optimization
}

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
}

function log(message, color = colors.reset) {
  console.log(`${color}${message}${colors.reset}`)
}

async function getAllImageFiles(dir) {
  const files = []

  async function walk(currentDir) {
    const entries = await readdir(currentDir, { withFileTypes: true })

    for (const entry of entries) {
      const fullPath = join(currentDir, entry.name)

      if (entry.isDirectory()) {
        await walk(fullPath)
      } else if (entry.isFile()) {
        const ext = extname(entry.name).toLowerCase()
        if (SUPPORTED_FORMATS.includes(ext)) {
          files.push(fullPath)
        }
      }
    }
  }

  await walk(dir)
  return files
}

async function getFileSize(filePath) {
  const stats = await stat(filePath)
  return stats.size
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

async function optimizeImage(inputPath, outputPath, width = null) {
  let pipeline = sharp(inputPath)

  // Get original dimensions
  const metadata = await pipeline.metadata()

  // Resize if width specified and image is larger
  if (width && metadata.width > width) {
    pipeline = pipeline.resize(width, null, {
      withoutEnlargement: true,
      fit: 'inside'
    })
  }

  // Convert to WebP with quality setting
  await pipeline
    .webp({ quality: QUALITY })
    .toFile(outputPath)
}

async function processImage(imagePath, stats) {
  const ext = extname(imagePath)
  const baseNameWithoutExt = basename(imagePath, ext)
  const dir = dirname(imagePath)

  log(`\n${colors.cyan}Processing: ${imagePath}${colors.reset}`)

  const originalSize = await getFileSize(imagePath)
  let totalSaved = 0
  let filesCreated = 0

  // Process each size variant
  for (const [sizeName, config] of Object.entries(SIZES)) {
    const outputFileName = `${baseNameWithoutExt}${config.suffix}.webp`
    const outputPath = join(dir, outputFileName)

    try {
      await optimizeImage(imagePath, outputPath, config.width)
      const newSize = await getFileSize(outputPath)
      const saved = originalSize - newSize
      totalSaved += saved
      filesCreated++

      const relativePath = outputPath.replace(PHOTOS_DIR, '').replace(/\\/g, '/')
      log(`  ${colors.green}✓${colors.reset} Created ${sizeName}: ${relativePath}`)
      log(`    Size: ${formatBytes(newSize)} (saved ${formatBytes(saved)})`)

      stats.totalSaved += saved
      stats.filesCreated++
    } catch (error) {
      log(`  ${colors.yellow}✗${colors.reset} Failed to create ${sizeName}: ${error.message}`)
    }
  }

  return { originalSize, totalSaved, filesCreated }
}

async function main() {
  log(`${colors.bright}${colors.blue}==============================================`)
  log(`  Image Optimization Script`)
  log(`==============================================${colors.reset}\n`)

  log(`Searching for images in: ${PHOTOS_DIR}`)

  if (!existsSync(PHOTOS_DIR)) {
    log(`${colors.yellow}Error: Photos directory not found!${colors.reset}`)
    process.exit(1)
  }

  // Find all images
  const imageFiles = await getAllImageFiles(PHOTOS_DIR)
  log(`\nFound ${colors.bright}${imageFiles.length}${colors.reset} images to process\n`)

  if (imageFiles.length === 0) {
    log(`${colors.yellow}No images found to process.${colors.reset}`)
    process.exit(0)
  }

  // Statistics
  const stats = {
    totalProcessed: 0,
    filesCreated: 0,
    totalSaved: 0,
    totalOriginalSize: 0
  }

  // Process each image
  for (const imagePath of imageFiles) {
    try {
      const result = await processImage(imagePath, stats)
      stats.totalProcessed++
      stats.totalOriginalSize += result.originalSize
    } catch (error) {
      log(`${colors.yellow}Error processing ${imagePath}: ${error.message}${colors.reset}`)
    }
  }

  // Print summary
  log(`\n${colors.bright}${colors.green}==============================================`)
  log(`  Optimization Complete!`)
  log(`==============================================${colors.reset}`)
  log(`Images processed: ${colors.bright}${stats.totalProcessed}${colors.reset}`)
  log(`WebP files created: ${colors.bright}${stats.filesCreated}${colors.reset}`)
  log(`Original total size: ${colors.bright}${formatBytes(stats.totalOriginalSize)}${colors.reset}`)
  log(`Total saved: ${colors.bright}${formatBytes(stats.totalSaved)}${colors.reset}`)

  if (stats.totalOriginalSize > 0) {
    const percentSaved = ((stats.totalSaved / stats.totalOriginalSize) * 100).toFixed(1)
    log(`Reduction: ${colors.bright}${colors.green}${percentSaved}%${colors.reset}\n`)
  }

  log(`${colors.cyan}Next steps:${colors.reset}`)
  log(`1. Update Vue components to use <picture> elements with WebP`)
  log(`2. Add loading="lazy" to off-screen images`)
  log(`3. Test image loading in the browser\n`)
}

main().catch(error => {
  log(`${colors.yellow}Fatal error: ${error.message}${colors.reset}`)
  process.exit(1)
})
