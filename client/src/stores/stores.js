import { writable } from "svelte/store";

export const mode = writable("light");
export const currentUser = writable({
  userId: 1714884,
  name: "Andy Tran",
  email: "aqtran@ualberta.ca",
});
export const authToken = writable("");
export const hasNotifications = writable(false);
export const isLoginPage = writable(false);
