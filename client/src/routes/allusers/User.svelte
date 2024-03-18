<script>
  import { onMount } from "svelte";
  import { currentUser, server, authToken } from "../../stores/stores.js";
  import { get } from "svelte/store";
  import { writable } from "svelte/store";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";

  export let user;
  const currentUserId = $currentUser.userId;
  const userId = user.id;
  const alreadyFollowed = writable(false);
  let alreadyFollowedValue;
  alreadyFollowed.subscribe((value) => {
    alreadyFollowedValue = value;
  });

  onMount(async () => {
    const followEndpoint = `${server}/api/follow/${userId}?userId2=${currentUserId}&senderHost=${server}&receiverHost=${user.host}`;
    console.log("currentUserId", currentUserId);
    console.log("target userId", userId);
    const response = await fetch(followEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${$authToken}`,
      },
    });
    if (!response.ok) {
      throw new Error("Failed to fetch follow status");
    }
    const data = await response.json();
    alreadyFollowed.set(data.following);
    console.log(currentUserId, "is", data.following, "following", userId);
  });

  // Follow or unfollow the user, also check for authentication
  async function followButtonClick() {
    console.log("clicked");
    console.log($currentUser);
    const followRequest = {
      userId1: currentUserId,
      userId2: userId,
      receiverHost: user.host,
      senderHost: server,
    };
    console.log("FOLLOW REQUEST:", followRequest);
    const headers = {
      Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
      "Content-Type": "application/json",
    };
    if (alreadyFollowedValue) {
      const response = await fetchWithRefresh(
        server + `/api/follow/${currentUserId}?userId2=${userId}`,
        {
          method: "DELETE",
          headers: headers,
          body: JSON.stringify(followRequest),
        }
      );
      if (!response.ok) {
        throw new Error("Failed to unfollow user");
      }
    } else {
      const response = await fetchWithRefresh(
        server + `/api/follow/${currentUserId}?userId2=${userId}`,
        {
          method: "POST",
          headers: headers,
          body: JSON.stringify(followRequest),
        }
      );
      if (!response.ok) {
        throw new Error("Failed to follow user");
      }
    }
    alreadyFollowed.update((value) => !value);
    console.log(
      "after clicking follow/unfollow, follow=",
      alreadyFollowedValue
    );
  }
</script>

<div class="user">
  <h3><strong>{user.displayName}</strong></h3>
  <p>Host: {user.host}</p>
  <img src={user.profileImage} alt={user.displayName + " profile pic"} />
  {#if currentUserId !== userId}
    {#if !$alreadyFollowed}
      <button class="follow-button" on:click={followButtonClick}>Follow</button>
    {:else}
      <button class="follow-button" on:click={followButtonClick}
        >Unfollow</button
      >
    {/if}
  {/if}
</div>

<style>
  .user {
    border: 1px solid #ccc;
    padding: 10px;
    width: 300px;
    color: black;
  }

  img {
    max-width: 100%;
    height: auto;
  }

  .follow-button {
    background-color: teal;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .follow-button:hover {
    background-color: darkcyan;
  }
</style>
