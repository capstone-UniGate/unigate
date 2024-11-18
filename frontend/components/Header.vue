<template>
  <header class="bg-blue-600 text-white p-4">
    <div class="container mx-auto flex items-center justify-between">
      <!-- Logo -->
      <div class="text-2xl font-bold">
        <router-link to="/" class="text-white">UniGate</router-link>
      </div>

      <!-- Desktop Navigation -->
      <nav class="hidden md:flex space-x-6">
        <router-link to="/" class="hover:text-blue-300">Home</router-link>
        <router-link to="/about" class="hover:text-blue-300">About</router-link>
        <router-link to="/contact" class="hover:text-blue-300"
          >Contact</router-link
        >
      </nav>

      <!-- Mobile Menu Button -->
      <button @click="toggleMenu" class="md:hidden text-white">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div
      v-if="isMenuOpen"
      class="md:hidden bg-blue-600 text-white p-4 space-y-4"
    >
      <router-link to="/" class="block hover:text-blue-300">Home</router-link>
      <router-link to="/about" class="block hover:text-blue-300"
        >About</router-link
      >
      <router-link to="/contact" class="block hover:text-blue-300"
        >Contact</router-link
      >
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
  },
};
</script>

<style scoped>
/* Optional custom styles */
</style>
