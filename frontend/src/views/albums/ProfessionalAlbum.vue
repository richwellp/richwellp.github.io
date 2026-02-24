<template>
  <AlbumViewer
    title="Me"
    icon="📷"
    subtitle="Personal moments, graduation, and career milestones"
    :photos="professionalPhotos"
  />
</template>

<script setup>
import AlbumViewer from '../../components/AlbumViewer.vue'
import { professionalPhotos } from '../../data/professionalPhotos'
</script>
