<script>
  import { onMount } from "svelte";
  import { currentUser, server, authToken } from "../../stores/stores.js";
  import { get } from "svelte/store";
  import { writable } from "svelte/store";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";

  // Props passed to the component
  export let profileImage; // A default image if none is provided
  export let name;
  export let email;
  export let github;
  export let userId; // The user ID passed into the component
  export let host;

  let shortGithub;
  let shortHost;
  // If github link is too long, create a shorter version of it for preview
  if (github.length > 25){
      shortGithub = github.slice(0, 25) + "..."
    } else {
      shortGithub = github
    }
    shortGithub = shortGithub.replace("https://", "")
    // If host link is too long, create a shorter version of it for preview
    if (host.length > 25){
      shortHost = host.slice(0, 25) + "..."
    } else {
      shortHost = host
    }


  // Get the current user's ID from the store
  const currentUserId = get(currentUser).userId;

  const path = window.location.pathname;
  const pathSegments = path.split("/");
  let target = pathSegments[pathSegments.length - 1];
  if (target != "all_users") {
    userId = target
  }

  // Check if the profile belongs to the current user
  let isCurrentUser = userId == currentUserId;

  // Initialize edit mode as a writable store
  const isEditMode = writable(false);
  let isEditModeValue;
  isEditMode.subscribe((value) => {
    isEditModeValue = value;
  });

  // Initialize form data as a writable store
  const formData = writable({
    name: name,
    email: email,
    github: github,
    profileImage: profileImage,
  });
  let formDataValue;
  formData.subscribe((value) => {
    formDataValue = value;
  });

  // Initialize alreadyFollowed as a writable store
  const alreadyFollowed = writable(false);
  let alreadyFollowedValue;
  alreadyFollowed.subscribe((value) => {
    alreadyFollowedValue = value;
  });
  onMount(async () => {
    const followEndpoint =
      server + `/api/follow/${userId}?userId2=${currentUserId}`;

    const response = await fetch(followEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${$authToken}`, // Include the token in the request headers
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
    const followRequest = {
      userId1: currentUserId,
      userId2: userId, //target user
      receiverHost: host + "/",
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

  async function saveProfile() {
    const updateEndpoint = server + `/api/profile/${userId}`;

    const response = await fetch(updateEndpoint, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
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
    profileImage = formDataValue.profileImage;

    isEditMode.set(false); // Close edit mode
    currentUser.update((value) => {
      return {
        ...value,
        name: formDataValue.name,
        email: formDataValue.email,
        github: formDataValue.github,
        profileImage: formDataValue.profileImage,
      };
    });
  }

  function cancelEdit() {
    isEditMode.set(false);
  }

  //const infoContainer = document.getElementById('profile-info');
  // Calculate the number of lines required for the text
  //const lines = Math.ceil(infoContainer.scrollHeight / parseFloat(getComputedStyle(infoContainer).lineHeight));
  //infoContainer.style.height = `${lines * parseFloat(getComputedStyle(infoContainer).lineHeight)}px`;

</script>

<div class="profile-widget">
  <img class="profile-image" src={profileImage} alt="Profile Avatar" />
  <div class="profile-info">
    {#if name}
      <div class="profile-name">{name}</div>
    {/if}
    {#if email}
      <div class="profile-email">Email: {email}</div>
    {/if}
    {#if github}
      {#if shortGithub}
        <div class="profile-github">Github: {shortGithub}</div>
      {:else}
        <div class="profile-github">Github: {github}</div>
      {/if}
    {/if}
    {#if host}
      <div class="profile-host">Host: {host}</div>
    {/if}
    {#if isCurrentUser && target=="all_users"}
      <button class="self-button">Yourself</button>
    {:else if !isCurrentUser}
      {#if !$alreadyFollowed}
        <button class="follow-button" on:click={followButtonClick}>Follow</button>
      {:else}
        <button class="follow-button" on:click={followButtonClick}>Unfollow</button>
      {/if}
    {:else if !isEditModeValue && target!="all_users"}
      <div class="flex justify-center">
        <button
          class="edit-button"
          on:click={() => {
            formData.set({
              name: name,
              email: email,
              github: github,
              profileImage: profileImage,
            });
            isEditMode.set(true);
          }}>Edit Profile</button
        >
      </div>
    {:else if isEditModeValue && isCurrentUser}
      <form on:submit|preventDefault={saveProfile}>
        <input
          type="text"
          class="profile-input"
          bind:value={formDataValue.name}
          placeholder="Name"
          title="Please enter your display name."
          required
        />
        <input
          type="email"
          class="profile-input"
          bind:value={formDataValue.email}
          placeholder="Email"
          required
        />
        <input
          type="text"
          class="profile-input"
          bind:value={formDataValue.github}
          placeholder="Github"
          required
        />
        <input
          type="text"
          class="profile-input"
          bind:value={formDataValue.profileImage}
          placeholder="Profile Image Url"
        />
        <div class="flex justify-center">
          <button class="save-button">Save Changes</button>
          <button type="button" class="cancel-button" on:click={cancelEdit}
            >Cancel</button
          >
        </div>
      </form>
    {/if}
  </div>
</div>

<style>
  .profile-widget {
    border: 1px solid #e1e1e1;
    border-radius: 0.5rem;
    padding: 1rem;
    text-align: center;
    width: 350px;
    margin: auto;
    color: black;
    /*height: 300px;
    width: 280px;*/
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
    overflow: hidden; /* Prevents content from overflowing */

    margin-left: 20px; /* Adjust as needed */
    margin-right: 20px; /* Adjust as needed */
  }

  .profile-name {
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 5px;
  }
  .profile-email {
    color: #555;
    font-size: 1em;
    margin-bottom: 3px;
  }
  .profile-github {
    color: #555;
    font-size: 1em;
    margin-bottom: 3px;
  }
  .profile-host {
    color: #555;
    font-size: 1em;
    margin-bottom: 3px;
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

  .self-button,
  .follow-button,
  .edit-button,
  .save-button,
  .cancel-button {
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

  .self-button,
  .follow-button,
  .edit-button {
    margin-top: 17px;
  }

  .self-button {
    background-color: rgb(119, 119, 119);
  }

  .follow-button:hover,
  .edit-button:hover,
  .save-button:hover,
  .cancel-button:hover {
    filter: brightness(85%);
  }

  /* Optional: Add a focus style for accessibility */
  .follow-button:focus,
  .edit-button:focus,
  .save-button:focus,
  .cancel-button:focus {
    outline: 3px solid #bbb;
    outline-offset: 2px;
  }
</style>
