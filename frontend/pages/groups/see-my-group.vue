<script setup>
import SeeMyGroup from "~/components/SeeMyGroup.vue";
</script>

<template>
  <div>
    <SeeMyGroup />
    <div v-if="isLoading" class="LoadingIndicator">Loading...</div>
    <div v-else class="groups-container">
      <div v-for="group in groups" :key="group.id" class="GroupCard">
        <!-- Card content -->
      </div>
    </div>
  </div>
</template>
