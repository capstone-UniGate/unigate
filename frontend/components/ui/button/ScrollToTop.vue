<template>
  <button
    v-if="isVisible"
    @click="scrollToTop"
    class="bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-2xl shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all mb-4 fixed bottom-4 right-6"
  >
    ↑
  </button>
</template>

<script>
export default {
  data() {
    return {
      isVisible: false,
    };
  },
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    toggleVisibility() {
      this.isVisible = window.scrollY > 200;
    },
  },
  mounted() {
    window.addEventListener("scroll", this.toggleVisibility);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.toggleVisibility);
  },
};
</script>

<style scoped>
button {
  font-size: 24px;
}
</style>
