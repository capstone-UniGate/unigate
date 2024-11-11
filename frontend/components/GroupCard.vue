<template>
    <div class="bg-white rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform">
      <!-- <img :src="image" alt="Group Image" class="w-full h-32 object-cover"> -->
      <img :src="`/static/images/${image}`" alt="Group Image" class="w-full h-32 object-cover" />

      <div class="p-4">
        <h2 class="text-lg font-bold text-gray-800 truncate">{{ name }}</h2>
        <p class="text-gray-600 text-sm mb-2">{{ description }}</p>
        
        <div class="text-gray-500 text-xs">
          <span>{{ members }} Members</span>
        </div>
        
        <div class="mt-3 flex space-x-2">
          <button
            class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600 transition-colors"
          >
            View Details
          </button>
          <button
            class="bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600 transition-colors"
          >
            Leave Group
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      name: {
        type: String,
        required: true,
      },
      description: {
        type: String,
        required: true,
      },
      members: {
        type: Number,
        required: true,
      },
      image: {
        type: String,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  /* Optionally add custom styling here if needed */
  </style>
  