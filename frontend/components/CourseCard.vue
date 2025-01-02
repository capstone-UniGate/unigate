<script setup lang="ts">
import { defineProps } from "vue";
import { useRouter } from "vue-router";

interface Course {
  name: string;
}

const props = defineProps<{ course: Course }>();
const router = useRouter();
const { getGroupById, checkAuthStatus } = useGroups();

</script>

<template>
  <div class="flex flex-wrap gap-4 justify-center">
    <Card
      height="330px"
      width="100%"
      v-if="course"
      class="max-w-sm flex flex-col h-full"
    >
      <div class="bg-stone-100 rounded-2xl m-4">
        <CardHeader>
          <div class="flex items-center space-x-5">
            <Avatar>
              <AvatarImage
                src="https://github.com/radix-vue.png"
                alt="@radix-vue"
              />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>
            <div class="flex-1 min-w-1">
              <CardTitle
                class="text-sm truncate overflow-hidden text-ellipsis whitespace-nowrap"
                >{{ course.name }}</CardTitle
              >
              <CardDescription
                class="text-xs truncate overflow-hidden text-ellipsis whitespace-nowrap"
                >{{ "group.category" }}</CardDescription
              >
            </div>
          </div>
        </CardHeader>
        <CardContent class="flex flex-col gap-5 mt-5 mr-5 mb-5 flex-grow">
          <p class="text-sm overflow-hidden line-clamp-2">
            {{ "group.description" }}
          </p>
          <p class="text-xs text-muted-foreground">
            Members: {{ "group.members_count" }}
          </p>
        </CardContent>
      </div>
    </Card>
  </div>
</template>

<style scoped></style>
