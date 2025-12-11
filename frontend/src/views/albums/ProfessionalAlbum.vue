<template>
  <AlbumViewer
    title="Professional"
    icon="💼"
    subtitle="Work events and milestones"
    :photos="professionalPhotos"
  />
</template>

<script setup>
import AlbumViewer from '../../components/AlbumViewer.vue'
import { professionalPhotos } from '../../data/professionalPhotos'
</script>
