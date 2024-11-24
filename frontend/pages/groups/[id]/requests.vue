<template>
  <div>
    <div v-if="requests" class="mx-auto max-w-5xl mt-10">
      <ul role="list" class="divide-y divide-gray-100">
        <li
          v-for="request in requests"
          :key="request.id"
          class="flex items-center justify-between gap-x-6 py-5"
        >
          <div class="flex min-w-0 gap-x-4 items-center">
            <img
              class="size-12 flex-none rounded-full bg-gray-50"
              :src="request.imageUrl || placeholderImage"
              alt=""
            />
            <div class="min-w-0 flex-auto">
              <p class="text-sm/6 font-semibold text-gray-900"></p>
            </div>
          </div>
          <div class="flex">
            <div v-if="request.status == 'PENDING'">
              <button
                @click="reject(request.id)"
                class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20 mr-10"
              >
                Reject
              </button>
              <button
                @click="approve(request.id)"
                class="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20"
              >
                Approve
              </button>
            </div>

            <div v-else>
              <span
                v-if="request.status == 'APPROVED'"
                class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20"
              >
                Approved
              </span>
              <span
                v-if="request.status == 'REJECTED'"
                class="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20"
              >
                Rejected
              </span>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <NoJoinRequest v-else />
  </div>
</template>

<script setup>
const route = useRoute();
const groupId = route.params.id;
const placeholderImage = "https://via.placeholder.com/150?text=Profile";
const requests = await useApiFetch(`groups/${groupId}/requests`);

function approve(id) {
  useApiFetch(`requests/${id}/approve`, {
    method: "post",
  });
}

function reject(id) {
  useApiFetch(`requests/${id}/reject`, {
    method: "post",
  });
}
</script>
