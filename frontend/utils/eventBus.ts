import { reactive } from "vue";

export const eventBus = reactive({
  photoUrl: "",
  username: "", // Add username storage
  updatePhoto(url: string) {
    this.photoUrl = url;
  },
  clearPhoto() {
    this.photoUrl = "";
  },
  setUsername(username: string) {
    this.username = username;
  },
  clearUsername() {
    this.username = "";
  },
});
