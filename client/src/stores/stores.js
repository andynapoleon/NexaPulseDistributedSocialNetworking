import { writable } from "svelte/store";

export const mode = writable("light");
export const currentUser = writable({
  userId: 1714884,
  name: "Andy Tran",
  email: "aqtran@ualberta.ca",
});
export const authToken = writable(localStorage.getItem("authToken") || "");
authToken.subscribe((val) => localStorage.setItem("authToken", val));
export const hasNotifications = writable(false);
export const isLoginPage = writable(false);
