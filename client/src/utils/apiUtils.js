// apiUtils.js

import { get } from "svelte/store";
import { authToken, refreshToken, server } from "../stores/stores"; // Assuming your stores are in a file named 'stores.js'

export async function fetchWithRefresh(url, options) {
  const response = await fetch(url, options);
  if (response.status === 401) {
    try {
      const tokenResponse = await fetch(server + "/api/token/refresh/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${get(refreshToken)}`,
        },
      });

      if (tokenResponse.ok) {
        const { access_token } = await tokenResponse.json();
        authToken.set(access_token);
        console.log("update", server + "/api/token/refresh");
        const retryResponse = await fetch(url, {
          ...options,
          headers: {
            ...options.headers,
            Authorization: `Bearer ${access_token}`,
          },
        });

        return retryResponse;
      } else {
        throw new Error("Failed to refresh token");
      }
    } catch (refreshError) {
      console.error("Error refreshing token:", refreshError);
      throw refreshError;
    }
  }

  return response;
}

export function extractUUID(url) {
  const parsedUrl = new URL(url);
  const pathSegments = parsedUrl.pathname.split("/");
  const uuid = pathSegments[pathSegments.length - 1]; // Assuming UUID is the last segment in the path
  return uuid;
}
