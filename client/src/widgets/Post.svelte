<script>
  import { currentUser, server, authToken } from '../stores/stores.js';
  import { fetchWithRefresh } from "../utils/apiUtils";
  import { get } from "svelte/store";

  let authorId = $currentUser.userId;
  let postId = '1';

  // Props passed to the component
  export let post;

  let userName = ""; // Initialize userName variable for the author's name
  let postTime = post.published;
  let content = post.content;
  let title = post.title;
  let likes = 0;

  // Local component state for editing
  let isEditing = false;
  let editedContent = post.content;
  let postTitle = title;

  // Fetch author's information based on authorId
  async function fetchAuthor() {
    try {
      const response = await fetch(`${server}/api/authors/${post.authorId}`);
      if (response.ok) {
        const authorData = await response.json();
        userName = `${authorData.firstName} ${authorData.lastName}`; // Set the userName to the author's display name
      } else {
        console.error('Failed to fetch author information:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching author information:', error.message);
    }
  }

  // Function to toggle edit mode
  function toggleEditMode() {
    isEditing = !isEditing;
    // Revert to original content if editing is canceled
    if (!isEditing) {
      post.content = editedContent;
    }
  }

  // Function to save edited content
  async function saveEdit() {
    const editPostEndpoint = server + `/api/authors/${authorId}/posts/${postId}/`;
    const response = await fetchWithRefresh(editPostEndpoint, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${get(authToken)}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title: postTitle, content: editedContent })
    });

    if (response.ok) {
      // Update the component state with edited content
      content = editedContent;
      title = postTitle;
      isEditing = false;
    } else {
      console.error('Failed to save edited post');
    }
    // content = editedContent;
    // isEditing = false;
  }

  // Fetch author's information when the component is mounted
  fetchAuthor();
</script>

<div class="post">
  <div class="post-header">
    <strong>Posted by {userName} {postTime}</strong>
  </div>
  <div class="post-title">
    {#if isEditing}
      <input type="text" bind:value={postTitle} />
    {:else}
      {title}
    {/if}
  </div>
  <div class="post-content">
    {#if isEditing}
      <textarea class="edit-content" bind:value={editedContent}></textarea>
    {:else}
      {content}
    {/if}
  </div>
  <div class="actions">
    <button>Like</button>
    <button>Share</button>
    <button on:click={toggleEditMode}>
      {isEditing ? "Cancel" : "Edit"}
    </button>
    {#if isEditing}
      <button on:click={saveEdit}>Save</button>
    {/if}
    <span>Likes: {likes}</span>
  </div>
</div>

<style>
  .post {
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 3%;
    color: black;
    width: 100%;
    font-size: large;
  }
  .post-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    color: grey;
    font-size: small;
  }
  .post-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 8px;
  }
  .post-content {
    margin-bottom: 12px;
  }
  .actions {
    display: flex;
    justify-content: left;
  }
  button {
    cursor: pointer;
    background-color: transparent;
    border: none;
    color: #008480;
    padding: 0;
    margin-right: 2%;
  }
  .edit-content {
    width: 100%;
    margin-bottom: 12px;
  }
</style>