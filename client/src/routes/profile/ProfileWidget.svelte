<script>
  import { onMount } from "svelte";
  import { currentUser, server, authToken } from "../../stores/stores.js";
  import { get } from "svelte/store";
  import { writable } from "svelte/store";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";

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


  // Initialize edit mode as a writable store
  const isEditMode = writable(false);
    let isEditModeValue;
    isEditMode.subscribe(value => {
      isEditModeValue = value;
    });

  // Initialize form data as a writable store
  const formData = writable({
      name: name,
      email: email,
      github: github,
    });
    let formDataValue;
    formData.subscribe(value => {
      formDataValue = value;
    });

  // Initialize alreadyFollowed as a writable store
  const alreadyFollowed = writable(false);
  let alreadyFollowedValue;
  alreadyFollowed.subscribe(value => {
    alreadyFollowedValue = value;
  });
  
  onMount(async () => {
    // Check if the current user is already following the user

    const followEndpoint = server + `/api/follow/${currentUserId}?userId2=${userId}`;
    
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

      alreadyFollowed.set(data.following);
    }
  );


  // Follow or unfollow the user, also check for authentication
  async function followButtonClick() {
    console.log("clicked")
    const followRequest = {
      userId1 : currentUserId,
      userId2 : userId,
    }; 
    const followEndpoint = server + `/api/follow/${currentUserId}`;
    const headers = {
      'Authorization': `Bearer ${get(authToken)}`, // Include the token in the request headers
      'Content-Type': 'application/json'
    };
    if (alreadyFollowedValue) {
      const response = await fetchWithRefresh(followEndpoint, {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify(followRequest),
      });
      if (!response.ok) { 
        throw new Error("Failed to follow user");
      }
    } else {
      const response = await fetchWithRefresh(followEndpoint, {
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
  async function saveProfile() {
    
    const updateEndpoint = server + `/api/profile/${userId}`;
    
    const response = await fetchWithRefresh(updateEndpoint, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${get(authToken)}`, // Include the token in the request headers
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formDataValue),
    });

    if (!response.ok) {
      throw new Error("Failed to update profile");
    }

    // Update the profile widget with the new data
    name = formDataValue.name;
    email = formDataValue.email;
    github = formDataValue.github;

    isEditMode.set(false); // Close edit mode
    currentUser.update((value) => {
      return {
        ...value,
        name: formDataValue.name,
        email: formDataValue.email,
        github: formDataValue.github,
      };
    });
  }

  function cancelEdit() {
    isEditMode.set(false);
  }
</script>


<div class="profile-widget">
  <img class="profile-image" src={profileImageUrl} alt="Profile Avatar" />
  <div class="profile-info">
    {#if !isCurrentUser}
      <div class="profile-name">{name}</div>
      <div class="profile-email">{email}</div>
      <div class="profile-github">{github}</div>
      {#if !$alreadyFollowed}
        <button class="follow-button" on:click={followButtonClick}
          >Follow</button
        >
      {:else}
        <button class="follow-button" on:click={followButtonClick}
          >Unfollow</button
        >
      {/if}
      
    {:else}
      {#if !isEditModeValue}
      <div class="profile-name">{name}</div>
      <div class="profile-email">{email}</div>
      <div class="profile-github">{github}</div>

      <div class="flex justify-center">
        <button class="edit-button" on:click={() => 
        {
          formData.set({
            name: name,
            email: email,
            github: github,
          });
          isEditMode.set(true)
        }
      }>Edit Profile</button>
      </div>
      {:else if isEditModeValue && isCurrentUser}
      <form on:submit|preventDefault={saveProfile}>
        <input type="text" class="profile-input" bind:value={formDataValue.name} placeholder="Name" pattern="^\S+\s+\S+$" title="Please enter your first and last name" required />
        <input type="email" class="profile-input" bind:value={formDataValue.email} placeholder="Email" required />
        <input type="text" class="profile-input" bind:value={formDataValue.github} placeholder="Github" required />
        <div class="flex justify-center">
          <button class="save-button">Save Changes</button>
          <button type="button" class="cancel-button" on:click={cancelEdit}>Cancel</button>
        </div>
      </form>
      {/if}
    {/if}
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

  .profile-input {
    width: 100%;
    padding: 0.5rem;
    margin: 0.5rem 0;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 0.25rem;
    transition: border-color 0.3s ease;
  }

  .follow-button, .edit-button, .save-button, .cancel-button{
    padding: 0.5rem 1rem;
    margin: 0.5rem;
    border: none;
    border-radius: 0.25rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 0.9em;
    background-color: teal; /* Twitter-like follow button color */
    color: white;
  }

  .follow-button:hover, .edit-button:hover, .save-button:hover, .cancel-button:hover{
    filter: brightness(85%);
  }

  /* Optional: Add a focus style for accessibility */
  .follow-button:focus, .edit-button:focus, .save-button:focus, .cancel-button:focus{
    outline: 3px solid #bbb;
    outline-offset: 2px;
  }
</style>
