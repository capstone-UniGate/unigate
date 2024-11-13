<script setup lang="ts">
import { defineEmits } from "vue";

const emit = defineEmits(["retry"]);
</script>

<template>
  <div class="text-center text-red-600">
    <p>Unable to load groups. Please try again later.</p>
    <Button @click="$emit('retry')" class="mt-4">
      <RefreshCcw class="mr-2 h-4 w-4" /> Retry
    </Button>
  </div>
</template>
