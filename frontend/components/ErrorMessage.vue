<script setup lang="ts">
import { defineEmits } from "vue";

const emit = defineEmits(["retry"]);
</script>

<template>
  <div class="text-center text-error">
    <p>Unable to load groups. Please try again later.</p>
    <Button @click="$emit('retry')" class="mt-4"> Retry </Button>
  </div>
</template>
