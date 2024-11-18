<template>
  <div class="layout-container">
    <!-- Header -->
    <Header />

    <!-- Main Content -->
    <main class="main-content">
      <slot />
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
import Header from "~/components/Header.vue";
import Footer from "~/components/Footer.vue";

export default {
  components: {
    Header,
    Footer,
  },
};
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Ensure the layout takes the full viewport height */
}

.main-content {
  flex: 1; /* This ensures the main content takes up all the available space */
}
</style>
