<template>
    <div class="container mx-auto p-6">
    <div class="flex justify-end mb-6 py-2">
        <h1 class="text-2xl font-semibold text-gray-800 mb-6">Your Enrolled Groups</h1>
        <Button class="ml-auto"><NuxtLink :to="`create`">Craete a new group</NuxtLink></Button>
    </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">

        <div v-for="group in groups" :key="group.id">

          <nuxt-link :to="`/group/${group.id}`">
            <SeeMyGroups :group="group" />
          </nuxt-link>
        </div>
      </div>
    </div>
  </template>

    <script setup>
    import SeeMyGroups from './../SeeMyGroups.vue';
    // import Button from '../..components/button/Button.vue';


    const groups = [
      { id: 1, name: 'Group 1' },
      { id: 2, name: 'Group 2' },
      { id: 3, name: 'Group 3' },
      { id: 4, name: 'Group 4' },
      { id: 5, name: 'Group 5' },
      { id: 6, name: 'Group 2' },
      { id: 7, name: 'Group 3' },
      { id: 8, name: 'Group 4' },
      { id: 9, name: 'Group 5' }
    ];
    </script>


    <style scoped>

    .container {
      max-width: 1200px;
    }
    </style>
