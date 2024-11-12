<template>
  <div class="app-container">
    <!-- <NuxtRouteAnnouncer /> -->
     <!-- <h1 class="font-serif | font-bold | text-3xl" >Welcome to UniGate!</h1> -->
    <!-- <Button>Button</Button> -->
    <!-- <NuxtRouteAnnouncer /> -->
    <Header />
    <div class="main-content">
      <NuxtPage />
    </div>
    <Footer />
  </div>
</template>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>