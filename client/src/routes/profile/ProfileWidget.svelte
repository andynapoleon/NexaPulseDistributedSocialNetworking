<script>
    import { onMount } from "svelte";
  import { currentUser, server } from "../../stores/stores.js";
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
    
    const response = await fetch(followEndpoint);
    if (!response.ok) {
      throw new Error("Failed to fetch follow status");
    }
    const data = await response.json();
    console.log("Following", data.following);
    alreadyFollowed.set(data.following);
  });

  // Follow or unfollow the user, also check for authentication
  async function followButtonClick() {
    const followRequest = {
      userId1 : currentUserId,
      userId2 : userId,
    }; 
    const followEndpoint = server + `/api/follow/`;
    const headers = {
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
    console.log("follow", alreadyFollowedValue);
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
  .profile-widget {
    border: 1px solid #e1e1e1;
    border-radius: 0.5rem;
    padding: 1rem;
    text-align: center;
    max-width: 18.75rem;
    margin: auto;
    color: black;
  }

  .profile-image {
    display: block;
    width: 6.25rem;
    height: 6.25rem;
    border-radius: 50%;
    margin-bottom: 1rem;
    object-fit: cover;
    margin-left: auto;
    margin-right: auto;
  }

  .profile-info {
    margin-bottom: 0.5rem;
  }

  .profile-name {
    font-size: 1.2em;
    font-weight: bold;
  }

  .profile-email {
    color: #555;
    font-size: 1em;
  }
  .profile-github {
    color: #555;
    font-size: 1em;
  }

  .follow-button {
    padding: 0.5rem 1rem;
    margin: 0.5rem;
    border: none;
    border-radius: 0.25rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 0.9em;
  }

  .follow-button {
    background-color: teal; /* Twitter-like follow button color */
    color: white;
  }

  .follow-button:hover{
    filter: brightness(85%);
  }

  /* Optional: Add a focus style for accessibility */
  .follow-button:focus{
    outline: 3px solid #bbb;
    outline-offset: 2px;
  }
</style>
