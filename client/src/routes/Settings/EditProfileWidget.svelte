<script>
    import { onMount } from "svelte";
    import { currentUser, server, authToken } from "../../stores/stores.js";
    import { get, writable } from "svelte/store";
  
    // Props passed to the component
    export let profileImageUrl; // A default image if none is provided
    export let name;
    export let email;
    export let github;

    
    // Get the current user's ID from the store
    const currentUserId = get(currentUser).userId;
  
    // Check if the profile belongs to the current user
    $: isCurrentUser = true;
  
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
  
    onMount(async () => {
      // If the user is editing their own profile, pre-fill the form with their current data
      if (isCurrentUser) {
        const userEndpoint = server + `/api/users/${currentUserId}`;
  
        const response = await fetch(userEndpoint, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${get(authToken)}`, // Include the token in the request headers
          },
        });
  
        if (!response.ok) {
          throw new Error("Failed to fetch user data");
        }
  
        const userData = await response.json();
        formData.set({
          name: userData.name,
          email: userData.email,
          github: userData.github,
        });
      }
    });
  
    async function saveProfile() {
      const updateEndpoint = server + `/api/users/${currentUserId}`;
  
      const response = await fetch(updateEndpoint, {
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
    }
  
    function cancelEdit() {
      isEditMode.set(false);
    }
  </script>
  
  <div class="profile-widget">
    <img class="profile-image" src={profileImageUrl} alt="Profile Avatar" />
    <div class="profile-info">
      {#if !isEditModeValue}
        <div class="profile-name">{name}</div>
        <div class="profile-email">{email}</div>
        <div class="profile-github">{github}</div>
      {:else}
        <input type="text" class="profile-input" bind:value={formDataValue.name} placeholder="Name" />
        <input type="email" class="profile-input" bind:value={formDataValue.email} placeholder="Email" />
        <input type="text" class="profile-input" bind:value={formDataValue.github} placeholder="Github" />
      {/if}
  
      <div class="flex justify-center">
        {#if isCurrentUser}
          {#if !isEditModeValue}
            <button class="edit-button" on:click={() => isEditMode.set(true)}>Edit Profile</button>
          {:else}
            <button class="save-button" on:click={saveProfile}>Save Changes</button>
            <button class="cancel-button" on:click={cancelEdit}>Cancel</button>
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
