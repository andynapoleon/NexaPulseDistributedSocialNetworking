<script>
    import { onMount } from "svelte";
  import { currentUser, server, authToken } from "../../stores/stores.js";
  import { get } from "svelte/store";
  import { writable } from "svelte/store";

  // Props passed to the component
  export let profileImageUrl; // A default image if none is provided
  export let name;
  export let email;
  export let github;
  export let userId; // The user ID passed into the component

  // Get the current user's ID from the store
  const currentUserId = get(currentUser).userId;

  // Check if the profile belongs to the current user
  $: isCurrentUser = userId == currentUserId;
  const path = window.location.pathname;
  const pathSegments = path.split('/');
  userId = parseInt(pathSegments[pathSegments.length - 1]);    

  // Initialize alreadyFollowed as a writable store
  const alreadyFollowed = writable(false);
  let alreadyFollowedValue;
  alreadyFollowed.subscribe(value => {
    alreadyFollowedValue = value;
  });
  
  onMount(async () => {
    // Check if the current user is already following the user
    const followEndpoint = server + `/api/follow/?userId1=${currentUserId}&userId2=${userId}`;
    
    const response = await fetch(followEndpoint, {
      method: "GET",
      headers: {
        'Authorization': `Bearer ${get(authToken)}`, // Include the token in the request headers
      }
    });
    if (!response.ok) {
      throw new Error("Failed to fetch follow status");
    }
    const data = await response.json();
    console.log("Following", data.following);
    alreadyFollowed.set(data.following);
  });

  // Follow or unfollow the user, also check for authentication
  async function followButtonClick() {
    console.log("clicked")
    const followRequest = {
      userId1 : currentUserId,
      userId2 : userId,
    }; 
    const followEndpoint = server + `/api/follow/`;
    const headers = {
      'Authorization': `Bearer ${get(authToken)}`, // Include the token in the request headers
      'Content-Type': 'application/json'
    };
    if (alreadyFollowedValue) {
      const response = await fetch(followEndpoint, {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify(followRequest),
      });
      if (!response.ok) { 
        throw new Error("Failed to follow user");
      }
    } else {
      const response = await fetch(followEndpoint, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(followRequest),
      });
      if (!response.ok) {
        throw new Error("Failed to follow user");
      }
    }
    
    alreadyFollowed.update((value) => !value);
    console.log("follow:", alreadyFollowedValue);
  }
</script>

<div class="profile-widget">
  <img class="profile-image" src={profileImageUrl} alt="Profile Avatar" />
  <div class="profile-info">
    <div class="profile-name">{name}</div>
    <div class="profile-email">{email}</div>
    <div class="profile-github">{github}</div>
    <div class="flex justify-center">
      {#if !isCurrentUser}
        {#if !$alreadyFollowed}
          <button class="follow-button" on:click={followButtonClick}
            >Follow</button
          >
        {:else}
          <button class="follow-button" on:click={followButtonClick}
            >Unfollow</button
          >
        {/if}
      {/if}
    </div>
  </div>
</div>

<style>
  @import "widgetStyle.css";
</style>
