<script setup lang="ts">
import { defineProps } from "vue";
import { useRouter } from 'vue-router';


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
const router = useRouter();
const goToGroupPage = () => {
  router.push(`/group/${props.group.id}`);
};
</script>

<template>
  <Card v-if="group" class="max-w-sm mx-auto flex flex-col h-full">
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
    </CardHeader>
    <CardContent class="grid gap-4">
      <p class="text-sm overflow-hidden line-clamp-2">{{ group.description }}</p>
      <p class="text-xs text-muted-foreground">
        Last activity: {{ group.recentActivity }}
      </p>
      <p class="text-xs text-muted-foreground">
        Members: {{ group.enrollmentCount }}
      </p>
    </CardContent>
    <CardFooter class="mt-auto p-0">
      <Button class="w-full" @click="goToGroupPage">View Group</Button>

    </CardFooter>
  </Card>
</template>
