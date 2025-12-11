# Album Media Data

This directory contains the media data for all album pages. The album system supports both photos and videos, making it easy to add new content by editing simple JavaScript files.

## How to Add Photos and Videos

### Travel Album (with categories/tabs)

**File:** `travelPhotos.js`

1. Add your image or video to `public/assets/photos/travel/<location>/`
2. Open `travelPhotos.js`
3. Add a new entry to the appropriate location array:

```javascript
export const travelPhotos = {
  wyoming: [
    {
      src: '/assets/photos/travel/wyoming/personal.JPG',
      caption: 'Wyoming highway adventures'
    },
    // Add new photo:
    {
      src: '/assets/photos/travel/wyoming/yellowstone.jpg',
      caption: 'Yellowstone National Park'
    },
    // Add new video (specify type: 'video'):
    {
      src: '/assets/photos/travel/wyoming/sunset.mp4',
      type: 'video',
      caption: 'Wyoming sunset timelapse'
    }
  ],
  // ... other locations
}
```

**Note:** Videos must include `type: 'video'`. Images can omit the type field or use `type: 'image'`.

**To add a new location tab:**

1. Add the location to `travelCategories`:
```javascript
export const travelCategories = [
  { id: 'wyoming', name: 'Wyoming' },
  { id: 'texas', name: 'Texas' } // New location
]
```

2. Add the location to `travelPhotos`:
```javascript
export const travelPhotos = {
  // ... existing locations
  texas: [
    { src: '/assets/photos/travel/texas/photo1.jpg', caption: 'Austin skyline' }
  ]
}
```

### Professional Album (simple grid, no tabs)

**File:** `professionalPhotos.js`

1. Add your image or video to `public/assets/photos/professional/`
2. Open `professionalPhotos.js`
3. Add a new entry to the array:

```javascript
export const professionalPhotos = [
  {
    src: '/assets/photos/professional/professional_0.jpg',
    caption: 'Graduation day at UIUC'
  },
  // Add new photo:
  {
    src: '/assets/photos/professional/conference2024.jpg',
    caption: 'Speaking at AI Conference 2024'
  },
  // Add new video:
  {
    src: '/assets/photos/professional/presentation.mp4',
    type: 'video',
    caption: 'Conference presentation'
  }
]
```

### Sports Album (simple grid, no tabs)

**File:** `sportsPhotos.js`

1. Add your image or video to `public/assets/photos/sports/`
2. Open `sportsPhotos.js`
3. Add a new entry to the array:

```javascript
export const sportsPhotos = [
  {
    src: '/assets/photos/sports/volleyball_tournament.jpg',
    caption: 'Volleyball tournament finals'
  },
  {
    src: '/assets/photos/sports/spike.mp4',
    type: 'video',
    caption: 'Game-winning spike'
  },
  {
    src: '/assets/photos/sports/deadlift_pr.jpg',
    caption: 'New deadlift PR - 500 lbs'
  }
]
```

4. **Remove the "Coming Soon" flag** in `SportsAlbum.vue`:
   - Open `frontend/src/views/albums/SportsAlbum.vue`
   - Remove the `coming-soon` and `coming-soon-message` props

## Architecture Overview

### File Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── AlbumViewer.vue          # Reusable album component
│   ├── data/
│   │   ├── travelPhotos.js          # Travel photo data
│   │   ├── professionalPhotos.js    # Professional photo data
│   │   └── sportsPhotos.js          # Sports photo data
│   └── views/
│       └── albums/
│           ├── TravelAlbum.vue      # Travel page (uses AlbumViewer)
│           ├── ProfessionalAlbum.vue # Professional page (uses AlbumViewer)
│           └── SportsAlbum.vue       # Sports page (uses AlbumViewer)
└── public/
    └── assets/
        └── photos/
            ├── travel/
            │   ├── wyoming/
            │   ├── colorado/
            │   └── ...
            ├── professional/
            └── sports/
```

### Benefits

1. **No code duplication** - One `AlbumViewer` component handles all albums
2. **Easy to add photos** - Just edit a data file
3. **Easy to add new albums** - Create a new data file and page (10 lines of code)
4. **Consistent styling** - Changes to `AlbumViewer` affect all albums
5. **Maintainable** - Logic, styling, and data are separated

## AlbumViewer Component

The `AlbumViewer` component accepts these props:

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `title` | String | Yes | Album title (e.g., "Travel") |
| `icon` | String | No | Emoji icon for the title |
| `subtitle` | String | No | Subtitle description |
| `photos` | Array/Object | Yes | Photo data (array for simple, object for categorized) |
| `categories` | Array | No | Category tabs (for albums with tabs) |
| `defaultCategory` | String | No | Initial category to show |
| `comingSoon` | Boolean | No | Show "Coming Soon" message instead of photos |
| `comingSoonMessage` | String | No | Custom "Coming Soon" message |

## Example: Creating a New Album

Let's say you want to add a "Food" album:

1. **Create data file:** `src/data/foodPhotos.js`
```javascript
export const foodPhotos = [
  { src: '/assets/photos/food/ramen.jpg', caption: 'Homemade ramen' }
]
```

2. **Create view file:** `src/views/albums/FoodAlbum.vue`
```vue
<template>
  <AlbumViewer
    title="Food"
    icon="🍜"
    subtitle="Culinary adventures and recipes"
    :photos="foodPhotos"
  />
</template>

<script setup>
import AlbumViewer from '../../components/AlbumViewer.vue'
import { foodPhotos } from '../../data/foodPhotos'
</script>
```

3. **Add route** in `src/router/index.js`:
```javascript
{
  path: '/misc/food',
  name: 'food-album',
  component: () => import('../views/albums/FoodAlbum.vue')
}
```

4. **Link to it** from the Misc page

That's it! Your new album is ready.

## Media Format Support

### Images
- **Formats**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Type field**: Optional (defaults to `'image'`)
- **Behavior**: Click to open in lightbox

### Videos
- **Formats**: `.mp4`, `.webm`, `.mov` (use `.mp4` for best compatibility)
- **Type field**: **Required** - must include `type: 'video'`
- **Grid behavior**: Auto-plays muted on loop when visible
- **Lightbox behavior**: Plays with controls, auto-plays with sound

### Tips
- Keep video file sizes reasonable (< 20MB recommended)
- Use video compression for web (H.264 codec for MP4)
- Videos show a black background in grid and lightbox
- Captions support plain text for both images and videos
- All styling is handled by the `AlbumViewer` component
- Media arrays can be empty (shows "No photos yet" message)
