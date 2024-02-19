<script>
  import { currentUser } from "../../stores/stores.js";
  import { get } from "svelte/store";
  import { writable } from "svelte/store";

  // Props passed to the component
  export let profileImageUrl = "default-profile.png"; // A default image if none is provided
  export let name = "John Doe";
  export let email = "john.doe@example.com";
  export let userId; // The user ID passed into the component

  // Get the current user's ID from the store
  const currentUserId = get(currentUser).userId;

  // Check if the profile belongs to the current user
  $: isCurrentUser = userId == currentUserId;

  // Initialize alreadyFollowed as a writable store
  const alreadyFollowed = writable(false);

  // Follow or unfollow the user
  function followButtonClick() {
    alreadyFollowed.update((value) => !value);
  }
</script>

<div class="profile-widget">
  <img class="profile-image" src={profileImageUrl} alt="Profile Avatar" />
  <div class="profile-info">
    <div class="profile-name">{name}</div>
    <div class="profile-email">{email}</div>
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
        <button class="add-friend-button">Add Friend</button>
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

  .follow-button,
  .add-friend-button {
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

  .add-friend-button {
    background-color: teal; /* Facebook-like add friend button color */
    color: white;
  }

  .follow-button:hover,
  .add-friend-button:hover {
    filter: brightness(85%);
  }

  /* Optional: Add a focus style for accessibility */
  .follow-button:focus,
  .add-friend-button:focus {
    outline: 3px solid #bbb;
    outline-offset: 2px;
  }
</style>
