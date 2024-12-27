import { reactive } from "vue";

export const eventBus = reactive({
  photoUrl: "",
  updatePhoto(url: string) {
    this.photoUrl = url;
  },
});
