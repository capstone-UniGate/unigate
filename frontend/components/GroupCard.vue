<script setup lang="ts">
import { defineProps } from "vue";
import { useRouter } from "vue-router";

// Define the Group interface with required fields
interface Group {
  name: string;
  category: string;
  id: string;
  description: string;
  recentActivity: string;
  members_count: number;
}

const props = defineProps<{ group: Group }>();
const router = useRouter();
const { getGroupById, checkAuthStatus } = useGroups();

const goToGroupPage = async () => {
  
  try {
    
    // First verify authentication status
    const isAuthenticated = await checkAuthStatus();
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }

    // Try to get group details
    const groupDetails = await getGroupById(props.group.id);
    if (groupDetails) {
      router.push(`/groups/${props.group.id}`);
    }
  } catch (error) {
    console.error("Error navigating to group:", error);
    // Only redirect to login for actual auth errors
    if (error.response?.status === 401 || error.response?.status === 403) {
      router.push("/login");
    }
  }
};
</script>

<template>
  <div class="flex flex-wrap gap-4 justify-center">
    <Card
      height="330px"
      width="100%"
      v-if="group"
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
                >{{ group.name }}</CardTitle
              >
              <CardDescription
                class="text-xs truncate overflow-hidden text-ellipsis whitespace-nowrap"
                >{{ group.category }}</CardDescription
              >
            </div>
          </div>
        </CardHeader>
        <CardContent class="flex flex-col gap-5 mt-5 mr-5 mb-5 flex-grow">
          <p class="text-sm overflow-hidden line-clamp-2">
            {{ group.description }}
          </p>
          <p class="text-xs text-muted-foreground">
            Members: {{ group.members_count }}
          </p>
        </CardContent>
      </div>
      <CardFooter class="mt-auto p-0 flex justify-center">
        <Button
          id="details"
          class="w-1/2 bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-2xl shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all mb-4"
          @click="goToGroupPage"
        >
          View Group
        </Button>
      </CardFooter>
    </Card>
  </div>
</template>

<style scoped></style>
