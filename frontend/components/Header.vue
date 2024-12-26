<template>
  <div>
    <header
      class="bg-light-blue-100/70 backdrop-blur-md border-b border-blue-300 fixed top-0 w-full z-50"
    >
      <div class="container mx-auto flex items-center justify-between p-4">
        <!-- Logo and Welcome Message -->
        <div class="flex items-center space-x-4">
          <div class="text-2xl font-bold flex items-center">
            <img
              src="../static/images/logo.png"
              alt="Logo"
              class="h-8 w-8 mr-2"
            />
            <router-link to="/homepage" class="text-blue-800"
              >UniGate</router-link
            >
          </div>
          <!-- Student Name -->
          <div
            v-if="isLoggedIn && currentStudent"
            class="text-blue-800 h-4 z-60"
          >
            Welcome, {{ currentStudent.name }}
          </div>
        </div>

        <!-- Desktop Navigation -->
        <nav
          class="hidden md:flex space-x-6 absolute left-1/2 transform -translate-x-1/2"
        >
          <router-link
            to="/homepage"
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

        <div class="flex items-center space-x-6">
          <!-- Logout Button (Desktop) -->
          <button
            v-if="isLoggedIn"
            @click="handleLogout"
            id="logout-button"
            class="hidden md:block bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
          >
            Logout
          </button>

          <!-- Updated Avatar with click handler -->
          <div class="cursor-pointer" @click="router.push('/user')">
            <Avatar>
              <AvatarImage
                src="https://github.com/radix-vue.png"
                alt="@radix-vue"
              />
              <AvatarFallback>{{ getInitials }}</AvatarFallback>
            </Avatar>
          </div>
        </div>

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
        <router-link to="/homepage" class="block hover:text-blue-500 transition"
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
          v-if="isLoggedIn"
          @click="handleLogout"
          class="block bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition text-center"
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

<script setup lang="ts">
import { useAuth } from "@/composables/useAuth";
import { useCurrentStudent } from "@/composables/useCurrentStudent";
import { onMounted, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

const { logout, isLoggedIn } = useAuth();
const { currentStudent, getCurrentStudent } = useCurrentStudent();
const router = useRouter();
const isMenuOpen = ref(false);

// Compute initials from student name
const getInitials = computed(() => {
  if (!currentStudent.value?.name) return "U";
  const names =
    `${currentStudent.value.name} ${currentStudent.value.surname}`.split(" ");
  return names
    .map((name) => name[0])
    .join("")
    .toUpperCase();
});

// Watch for login state changes
watch(isLoggedIn, async (newValue) => {
  if (newValue) {
    await getCurrentStudent();
  } else {
    currentStudent.value = null;
  }
});

onMounted(async () => {
  if (isLoggedIn.value) {
    await getCurrentStudent();
  }
});

const handleLogout = async () => {
  try {
    await logout();
    currentStudent.value = null;
    await router.push("/login?message=You have successfully logged out.");
  } catch (error) {
    console.error("Logout error:", error);
  }
};
const toggleMenu = async () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>

<style scoped></style>
