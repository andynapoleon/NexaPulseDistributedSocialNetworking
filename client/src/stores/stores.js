import { writable, get, readable } from "svelte/store";

export const mode = writable("light");
export const server = "http://127.0.0.1:8000";
// http://127.0.0.1:5000
// https://nexapulse-25959148b934.herokuapp.com (viet)
// https://nexapulse1-7fbca99d2d7b.herokuapp.com (andy)
// Retrieve user data from localStorage if available
const storedUserData = localStorage.getItem("userData");
const initialUserData = storedUserData
  ? JSON.parse(storedUserData)
  : {
      userId: 1714884,
      name: "Andy Tran",
      email: "aqtran@ualberta.ca",
      github: "",
      lastUpdated: new Date(2024, 0, 3),
    };
if (
  initialUserData.lastUpdated === null ||
  initialUserData.lastUpdated === undefined
) {
  initialUserData.lastUpdated = new Date(2024, 0, 3);
}
export const currentUser = writable(initialUserData);

// Function to get the current value of currentUser
export function getCurrentUser() {
  return get(currentUser);
}

export const authToken = writable(localStorage.getItem("authToken") || "");
export const refreshToken = writable(
  localStorage.getItem("refreshToken") || ""
);

authToken.subscribe((val) => localStorage.setItem("authToken", val));
refreshToken.subscribe((val) => localStorage.setItem("refreshToken", val));
// Subscribe to changes in currentUser and update localStorage
currentUser.subscribe((value) => {
  localStorage.setItem("userData", JSON.stringify(value));
});

export const hasNotifications = writable(false);
export const isLoginPage = writable(false);

export const posts = writable([]);
export const followingPosts = writable([]);
export const followRequests = writable([]);
