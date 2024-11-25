<script setup lang="ts">
import { ScrollArea } from "@/components/ui/scroll-area";
//import { Separator } from "@/components/ui/separator";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const groupId = route.params.id;

// Mock members (call API)
const groupMembers = [
  { id: 1, name: "Alice" },
  { id: 2, name: "Bob" },
  { id: 3, name: "Charlie" },
  { id: 4, name: "David" },
];
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Members of Group {{ groupId }}</h1>

    <ScrollArea class="h-72 w-full rounded-md border p-4">
      <div v-for="member in groupMembers" :key="member.id">
        {{ member.name }}
        <Separator class="my-2" data-testid="{{ member.name }}" />
      </div>
    </ScrollArea>
  </div>
</template>

<style scoped>
.p-6 {
  padding: 1.5rem;
}
.border {
  border: 1px solid #e5e7eb;
}
.text-blue-600 {
  color: #2563eb;
}
.text-blue-600:hover {
  text-decoration: underline;
}
</style>
