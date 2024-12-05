<template>
  <div>
    <header
      class="bg-light-blue-100/70 backdrop-blur-md border-b border-blue-300 fixed top-0 w-full z-50"
    >
      <div class="container mx-auto flex items-center justify-between p-4">
        <!-- Logo -->
        <div class="text-2xl font-bold flex items-center">
          <img
            src="../static/images/logo.png"
            alt="Logo"
            class="h-8 w-8 mr-2"
          />
          <router-link to="/" class="text-blue-800">UniGate</router-link>
        </div>

        <!-- Desktop Navigation -->
        <nav
          class="hidden md:flex space-x-6 absolute left-1/2 transform -translate-x-1/2"
        >
          <router-link
            to="/"
            class="text-blue-800 hover:text-blue-500 transition"
            >Home</router-link
          >
          <router-link
            to="/about"
            class="text-blue-800 hover:text-blue-500 transition"
            >About</router-link
          >
          <router-link
            to="/contact"
            class="text-blue-800 hover:text-blue-500 transition"
            >Contact</router-link
          >
        </nav>

        <!-- Logout Button (Desktop) -->
        <button
          @click="logout"
          class="hidden md:block bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
        >
          Logout
        </button>

        <!-- Mobile Menu Button -->
        <button @click="toggleMenu" class="md:hidden text-blue-800">
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
        class="md:hidden bg-light-blue-100 text-blue-800 p-4 space-y-4 border-t border-blue-300"
      >
        <router-link to="/" class="block hover:text-blue-500 transition"
          >Home</router-link
        >
        <router-link to="/about" class="block hover:text-blue-500 transition"
          >About</router-link
        >
        <router-link to="/contact" class="block hover:text-blue-500 transition"
          >Contact</router-link
        >
        <!-- Logout Button (Mobile) -->
        <button
          @click="logout"
          class="block bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition w-full text-center"
        >
          Logout
        </button>
      </div>
    </header>

    <main class="pt-16">
      <!-- Main content here -->
    </main>
  </div>
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
    logout() {
      console.log("Logging out...");
      localStorage.removeItem("authToken");
      // Redirect to login page with a success message
      this.$router.push({
        path: "/login",
        query: { message: "You have successfully logged out." },
      });
    },
  },
};
</script>

<style scoped></style>
