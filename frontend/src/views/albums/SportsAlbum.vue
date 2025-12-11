<template>
  <AlbumViewer
    title="Sports"
    icon="🏐"
    subtitle="Volleyball and powerlifting adventures"
    :photos="sportsPhotos"
    coming-soon
    coming-soon-message="Photos from volleyball matches and powerlifting sessions will be added here!"
  />
</template>

<script setup>
import AlbumViewer from '../../components/AlbumViewer.vue'
import { sportsPhotos } from '../../data/sportsPhotos'
</script>
