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

// Define props with TypeScript, ensuring `group` matches the Group interface
const props = defineProps<{ group: Group }>();
</script>

<template>
  <Card v-if="group" class="max-w-sm mx-auto">
    <CardHeader>
      <div class="flex items-center space-x-5">
        <Avatar>
          <AvatarImage
            src="https://github.com/radix-vue.png"
            alt="@radix-vue"
          />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
        <div>
          <CardTitle class="text-md">{{ group.name }}</CardTitle>
          <CardDescription>{{ group.category }}</CardDescription>
        </div>
      </div>
      <!-- <div>
        <Avatar>
          <AvatarImage
            src="https://github.com/radix-vue.png"
            alt="@radix-vue"
          />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
        <CardTitle>{{ group.name }}</CardTitle>
        <CardDescription>{{ group.category }}</CardDescription>
      </div> -->
    </CardHeader>
    <CardContent class="grid gap-4">
      <p class="text-sm">{{ group.description }}</p>
      <p class="text-xs text-muted-foreground">
        Last activity: {{ group.recentActivity }}
      </p>
      <p class="text-xs text-muted-foreground">
        Members: {{ group.enrollmentCount }}
      </p>
    </CardContent>
    <CardFooter>
      <Button class="w-full">View Group</Button>
    </CardFooter>
  </Card>
</template>
