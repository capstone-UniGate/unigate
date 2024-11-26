<template>
  <div
    class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 text-center px-4"
  >
    <!-- Blocked Header -->
    <div class="bg-white shadow-lg rounded-lg p-6 max-w-lg w-full">
      <h1 class="text-4xl font-bold text-red-600 mb-4">You Are Blocked</h1>
      <p class="text-gray-700 text-lg leading-relaxed">
        You have been blocked from accessing this group. If you believe this is
        a mistake, please contact the group administrator.
      </p>
    </div>

    <!-- Return to Home Button -->
    <NuxtLink
      to="/"
      class="mt-8 bg-gradient-to-r from-indigo-500 to-blue-600 text-white font-medium px-6 py-3 rounded-lg shadow-lg hover:from-blue-600 hover:to-blue-700 hover:shadow-xl active:scale-95 transition-all"
    >
      Return to Home
    </NuxtLink>
  </div>
</template>

<style scoped>
/* Styling for Animation */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

div {
  animation: fade-in 0.3s ease-in-out;
}
</style>
