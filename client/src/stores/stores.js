import { writable } from "svelte/store";

export const mode = writable("light");
export const userId = writable(null);
export const token = writable(null);
export const hasNotifications = writable(false);
