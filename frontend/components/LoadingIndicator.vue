<template>
  <div class="text-center">
    <!-- Spinner -->
    <div
      class="inline-block w-12 h-12 border-4 border-t-transparent border-primary rounded-full animate-spin"
    ></div>
    <!-- Loading Text -->
    <p class="mt-4">Loading...</p>
  </div>
</template>

<script>
export default {
  name: "LoadingIndicator",
};
</script>
