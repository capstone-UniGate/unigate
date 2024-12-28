<template>
  <footer class="bg-stone-100 text-blue-800 py-1 border border-blue-300">
    <div class="container mx-auto text-center">
      <!-- Logo Section -->
      <div class="text-2xl font-bold mb-4">
        <router-link to="/" class="text-blue-800">UniGate</router-link>
      </div>

      <!-- Navigation Links -->
      <div class="flex justify-center space-x-8 text-sm font-light mb-4">
        <router-link to="/homepage" class="hover:text-blue-500"
          >Home</router-link
        >
        <router-link to="/about" class="hover:text-blue-500">About</router-link>
        <router-link to="/contact" class="hover:text-blue-500"
          >Contact Us</router-link
        >
      </div>

      <!-- Footer Bottom -->
      <div class="mt-6 text-xs text-gray-600">© 2024 Knowledge Collective</div>
    </div>
    <ScrollToTop />
  </footer>
</template>

<script>
import ScrollToTop from "./ui/button/ScrollToTop.vue";

export default {
  name: "Footer",
  components: {
    ScrollToTop,
  },
};
</script>

<style scoped>
/* Add padding and spacing adjustments */
footer {
  font-family: "Arial", sans-serif;
}
</style>
