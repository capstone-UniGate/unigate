<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 class="text-4xl font-bold text-yellow-600 mb-4">Access Denied</h1>
      <p class="text-gray-700 text-lg">
        You have been rejected from this private group. If you believe this is a mistake, please contact the group administrator.
      </p>
      <NuxtLink
        to="/"
        class="mt-6 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
        Return to Home
      </NuxtLink>
    </div>
  </template>
