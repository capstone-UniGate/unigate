import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/pages/index.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/pages/login.vue"),
    },
    {
      path: "/groups",
      name: "groups",
      component: () => import("@/components/GroupList.vue"),
    },
    {
      path: "/groups/create",
      name: "create-group",
      component: () => import("@/pages/groups/create.vue"),
    },
    {
      path: "/groups/:id/requests",
      name: "request",
      component: () => import("@/pages/groups/[id]/requests.vue"),
    },
    {
      path: "/groups/:id",
      name: "group-details",
      component: () => import("@/pages/groups/[id].vue"),
    },
    {
      path: "/my-groups",
      name: "my-groups",
      component: () => import("@/components/SeeMyGroup.vue"),
    },
    // Error handling routes
    {
      path: "/404",
      name: "not-found",
      component: () => import("@/pages/404.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      redirect: "/404",
    },
  ],
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  // Add authentication logic here if needed
  next();
});

export default router;
