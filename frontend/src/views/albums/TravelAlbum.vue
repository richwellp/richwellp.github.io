<template>
  <AlbumViewer
    title="Travel"
    icon="✈️"
    subtitle="Adventures around the world"
    :photos="travelPhotos"
    :categories="travelCategories"
    default-category="wyoming"
  />
</template>

<script setup>
import AlbumViewer from '../../components/AlbumViewer.vue'
import { travelPhotos, travelCategories } from '../../data/travelPhotos'
</script>
