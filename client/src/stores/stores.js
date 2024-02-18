import { writable } from "svelte/store";

export const mode = writable("light");
export const currentUser = writable({
  userId: null,
  name: "",
  email: "",
});
export const token = writable(null);
export const hasNotifications = writable(false);
