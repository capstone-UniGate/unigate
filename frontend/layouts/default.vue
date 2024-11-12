<template>
    <div>
      <!-- Header -->
      <Header />

      <!-- Main Content -->
      <main>
        <Nuxt />
      </main>

      <!-- Footer -->
      <Footer />
    </div>
  </template>

  <script>
  import Header from '~/components/Header.vue';
  import Footer from '~/components/Footer.vue';

  export default {
    components: {
      Header,
      Footer,
    },
  };
  </script>

  <style scoped>
  /* Optional custom styles */
  </style>
