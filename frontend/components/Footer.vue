<template>
    <footer class="bg-gray-800 text-white py-6">
      <div class="container mx-auto text-center">
        <p class="text-sm">© 2024 MySite. All Rights Reserved.</p>

        <!-- Links for Desktop -->
        <div class="hidden md:flex justify-center space-x-8 mt-4">
          <router-link to="/" class="hover:text-blue-300">Home</router-link>
          <router-link to="/about" class="hover:text-blue-300">About</router-link>
          <router-link to="/contact" class="hover:text-blue-300">Contact</router-link>
        </div>

        <!-- Social Media Icons (Optional) -->
        <div class="flex justify-center space-x-6 mt-4">
          <a href="#" class="text-white hover:text-blue-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 3v18M6 3l4 4-4 4M18 3v18M18 3l-4 4 4 4" />
            </svg>
          </a>
          <a href="#" class="text-white hover:text-blue-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 3v18M6 3l4 4-4 4M18 3v18M18 3l-4 4 4 4" />
            </svg>
          </a>
        </div>
      </div>
    </footer>
  </template>

  <script>
  export default {
    name: 'Footer',
  };
  </script>

  <style scoped>
  /* Optional custom styles */
  </style>

