<template>
  <Header />
    <div class="container mx-auto p-6">
      <h1 class="text-2xl font-semibold text-gray-800 mb-6">Your Enrolled Groups</h1>
  
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <GroupCard
          v-for="group in groups"
          :key="group.id"
          :name="group.name"
          :description="group.description"
          :members="group.members"
          :image="group.image"
        />
      </div>
    </div>
    <Footer />
  </template>
  
  <script>
  import GroupCard from '~/components/GroupCard.vue';
  
  export default {
    components: {
    GroupCard,
    name: 'IndexPage',
    },
    data() {
      return {
        groups: [
          {
            id: 1,
            name: 'Book Lovers',
            description: 'A group for those who love reading and sharing books.',
            members: 123,
            image: '',
          },
          {
            id: 2,
            name: 'Hiking Enthusiasts',
            description: 'Join us for regular hikes and outdoor adventures.',
            members: 89,
            image: '',
          },
          {
            id: 3,
            name: 'Hiking Enthusiasts',
            description: 'Join us for regular hikes and outdoor adventures.',
            members: 89,
            image: 'study-group-test.png',
          },
          {
            id: 4,
            name: 'Hiking Enthusiasts',
            description: 'Join us for regular hikes and outdoor adventures.',
            members: 89,
            image: '/images/study-group-test.png',
          },
          {
            id: 5,
            name: 'Hiking Enthusiasts',
            description: 'Join us for regular hikes and outdoor adventures.',
            members: 89,
            image: '/images/study-group-test.png',
          },
          {
            id: 5,
            name: 'Hiking Enthusiasts',
            description: 'Join us for regular hikes and outdoor adventures.',
            members: 89,
            image: '/images/study-group-test.png',
          },
          {
            id: 5,
            name: 'Hiking Enthusiasts',
            description: 'Join us for regular hikes and outdoor adventures.',
            members: 89,
            image: '/images/study-group-test.png',
          },
          {
            id: 5,
            name: 'Hiking Enthusiasts',
            description: 'Join us for regular hikes and outdoor adventures.',
            members: 89,
            image: '/images/study-group-test.png',
          }
          // Add more group objects as needed
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  
  .container {
    max-width: 1200px;
  }
  </style>
