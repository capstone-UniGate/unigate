<script setup lang="ts">
import type { HTMLAttributes } from "vue";
import { cn } from "@/lib/utils";

const props = defineProps<{
  class?: HTMLAttributes["class"];
  height?: string;
  width?: string;
}>();
</script>

<template>
  <div
    :class="
      cn('rounded-2xl border text-card-foreground shadow-sm', props.class)
    "
    :style="{ height: props.height, width: props.width }"
  >
    <slot />
  </div>
</template>
