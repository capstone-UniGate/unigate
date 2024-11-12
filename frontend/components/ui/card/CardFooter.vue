<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <div :class="cn('flex items-center p-6 pt-0', props.class)">
    <div class="mt-4 flex space-x-2">
          <button
            class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600 transition-colors">
            View Details
          </button>
        </div>
  </div>
</template>
