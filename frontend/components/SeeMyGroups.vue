<script setup lang="ts">
import { defineProps } from "vue";

// Define the Group interface with required fields
interface Group {
  name: string;
  category: string;
  description: string;
  recentActivity: string;
  enrollmentCount: number;
}

const props = defineProps<{ group: Group }>();
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Group Name</CardTitle>
      <CardDescription>Group Description</CardDescription>
    </CardHeader>
    <CardContent> Card Content </CardContent>
    <CardFooter> Card Footer </CardFooter>
  </Card>
</template>
