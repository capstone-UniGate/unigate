<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold text-blue-800">Welcome to UniGate</h1>
    <div v-if="isLoggedIn && currentStudent" class="mt-4 text-xl text-blue-600">
      Hello, {{ currentStudent.name }}!
    </div>
    <div v-else class="mt-4 text-xl text-blue-600">
      Please log in to see your information.
    </div>
  </div>
</template>

<script>
import { useAuth } from "@/composables/useAuth";
import { useCurrentStudent } from "@/composables/useCurrentStudent";
import { onMounted } from "vue";

export default {
  setup() {
    const { isLoggedIn } = useAuth();
    const { currentStudent, getCurrentStudent } = useCurrentStudent();

    onMounted(() => {
      if (isLoggedIn) {
        getCurrentStudent();
      }
    });

    return {
      isLoggedIn,
      currentStudent,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
}
</style>
