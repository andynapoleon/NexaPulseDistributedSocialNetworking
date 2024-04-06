<script>
  import { currentUser, server, authToken } from "../stores/stores.js";
  import { fetchWithRefresh } from "../utils/apiUtils";
  import { get } from "svelte/store";
  import { posts } from "../stores/stores.js";
  import { createEventDispatcher } from "svelte";
  import { navigate } from "svelte-routing";
  import { onMount, onDestroy } from "svelte";
  import { marked } from "../../node_modules/marked";

  // Props passed to the component
  export let post;
  const dispatch = createEventDispatcher();

  let userName = "";
  let time = new Date(post.published)
  let postTime = time.toLocaleString();
  let content = post.content;
  let title = post.title;
  let authorId = $currentUser.userId;
  let postId = post.id;
  export let likeCount = 0;
  export let commentCount = 0;
  let sharedBy = post.sharedBy;
  let isShared = post.isShared;
  let thoughts = "This post is so good!";
  let originalAuthor = "";
  let originalContent = post.originalContent;
  let image_base64 = "";
  let image_type = "";

  // Local component state for editing
  let isLiked = false;
  let isEditing = false;
  let editedContent = post.content;
  let postTitle = title;

  // Comment state
  let isCommenting = false;
  let commentText = "";

  function editPostId(postId) {
    return postId.split("/").pop();
  }

  postId = editPostId(postId);

  // Fetch author's information based on authorId
  async function fetchAuthor() {
    try {
      // console.log(`I AM HERE???!`);
      console.log(`${post.authorId}`);
      const response = await fetchWithRefresh(
        `${server}/api/authors/${post.authorId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${get(authToken)}`,
          },
        }
      );
      if (response.ok) {
        const authorData = await response.json();
        userName = `${authorData.displayName}`;
      } else {
        console.error(
          "Failed to fetch author information:",
          response.statusText
        );
      }
    } catch (error) {
      console.error("Error fetching author information:", error.message);
    }
  }

  // Fetch author's information based on authorId
  async function fetchOriginalAuthor() {
    try {
      const response = await fetchWithRefresh(
        `${server}/api/authors/${sharedBy}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${get(authToken)}`,
          },
        }
      );
      if (response.ok) {
        const authorData = await response.json();
        originalAuthor = `${authorData.displayName}`;
      } else {
        console.error(
          "Failed to fetch author information:",
          response.statusText
        );
      }
    } catch (error) {
      console.error("Error fetching author information:", error.message);
    }
  }

  // Function to fetch comment count - returns a list of comments
  async function fetchComments() {
    try {
      const response = await fetchWithRefresh(
        `${server}/api/authors/${authorId}/posts/${postId}/comments`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${get(authToken)}`,
          },
        }
      );
      if (response.ok) {
        const comments = await response.json();
        commentCount = comments.length;
      } else {
        console.error("Failed to fetch comment count:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching comment count:", error.message);
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
    const editPostEndpoint =
      server + `/api/authors/${authorId}/posts/${postId}/`;
    const response = await fetchWithRefresh(editPostEndpoint, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${get(authToken)}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: postTitle,
        content: editedContent,
        image: "",
      }),
    });

    if (response.ok) {
      // Update the component state with edited content
      content = editedContent;
      title = postTitle;
      isEditing = false;
    } else {
      console.error("Failed to save edited post");
    }
    // content = editedContent;
    // isEditing = false;
  }

  // Function to delete the post
  async function deletePost() {
    if (confirm("Are you sure you want to delete this post?")) {
      const deletePostEndpoint = `${server}/api/authors/${authorId}/posts/${postId}/`;
      const response = await fetchWithRefresh(deletePostEndpoint, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${get(authToken)}`,
        },
      });

      if (response.ok) {
        dispatch("changed", { changeDetected: true });
      } else {
        console.error("Failed to delete post:", response.statusText);
      }
    }
  }

  // Define a function to handle post details redirection
  function goToPostDetails(postId) {
    postId = editPostId(postId);
    navigate(`/posts/${postId}`);
  }

  // Fetch the number of likes for the post
  async function fetchLikes() {
    try {
      const response = await fetchWithRefresh(
        `${server}/api/authors/${authorId}/posts/${postId}/listoflikes`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${get(authToken)}`,
          },
        }
      );

      if (response.ok) {
        const likes = await response.json();
        likeCount = likes.length;
        isLiked = likes.some((like) => like.author === authorId);
      } else {
        console.error("Failed to fetch likes:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching likes:", error.message);
    }
  }

  async function toggleLike() {
    try {
      if (isLiked) {
        // Unlike the post
        const response = await fetchWithRefresh(
          `${server}/api/authors/${authorId}/inbox/`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${get(authToken)}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ author: post.authorId, post: postId }),
          }
        );

        if (response.ok) {
          isLiked = false;
          fetchLikes();
        } else {
          console.error("Failed to unlike the post:", response.statusText);
        }
      } else {
        // Like the post
        const response = await fetchWithRefresh(
          `${server}/api/authors/${authorId}/inbox/`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${get(authToken)}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ author: post.authorId, post: postId }),
          }
        );

        if (response.ok) {
          isLiked = true;
          fetchLikes();
        } else {
          console.error("Failed to like the post:", response.statusText);
        }
      }
    } catch (error) {
      console.error("Error toggling like:", error.message);
    }
  }

  async function fetchPostImage() {
    try {
      const response = await fetch(
        `${server}/api/authors/${authorId}/posts/${postId}/image`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${$authToken}`,
          },
        }
      );
      if (response.ok) {
        const post = await response.json();
        image_base64 = post.content;
        image_type = post.contentType;
      } else {
        console.error("Failed to fetch image:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching image:", error.message);
    }
  }

  let containerClass;
  // Update UI for container for post
  function updateContainerClass() {
    var list = document.querySelectorAll('aside');
    console.log("sideBar width:", list[0].offsetWidth)

    console.log("post containerClass:", containerClass)

    if (window.innerWidth > 1000) { // = 700/0.7
      containerClass = "post-big";
    } else if (window.innerWidth > 643){ // = 450/0.7
      containerClass = "post-mid";
    } else {
      containerClass = "post-small";
    }
  }

  onMount(() => {
    updateContainerClass();
    window.addEventListener('resize', updateContainerClass);
  });

  onDestroy(() => {
    window.removeEventListener('resize', updateContainerClass);
  });

  // Fetch the image associated with the post when the component is mounted
  onMount(() => {
    fetchAuthor();
    if (post.image_ref) {
      fetchPostImage();
    }
  });

  // Fetch author's information when the component is mounted

  fetchComments();
  fetchLikes();
  fetchOriginalAuthor();
</script>

<div class={containerClass}>
  <div class="post-header">
    <strong>Shared by {userName} {postTime}</strong>
  </div>
  <div class="post-content">
    {#if isEditing}
      <textarea class="edit-content" bind:value={editedContent}></textarea>
    {:else}
      {@html marked(post.content)}
    {/if}
  </div>
  <div class="post-header">
    <strong>Posted by {originalAuthor}</strong>
  </div>
  <div class="border-cyan-400">
    <div class="post-title">
      {#if isEditing}
        <input type="text" bind:value={postTitle} />
      {:else}
        {title}
      {/if}
    </div>
    <div class="post-content">
      {#if post.image_ref}
        <img src="data:{image_type}, {image_base64}" alt=" " />
      {/if}
      {originalContent}
    </div>
  </div>
  <div class="actions">
    {#if isLiked}
      <button on:click={toggleLike}>Unlike</button>
    {:else}
      <button on:click={toggleLike}>Like</button>
    {/if}
    <!-- <button on:click={toggleCommentMode}> Comment </button> -->
    <button on:click={() => goToPostDetails(post.id)}> Comment </button>
    {#if post.authorId == authorId}
      <button on:click={toggleEditMode}>
        {isEditing ? "Cancel" : "Edit"}
      </button>
      {#if isEditing}
        <button on:click={saveEdit}>Save</button>
      {/if}
    {/if}
    {#if post.authorId == authorId}
      <button on:click={deletePost}>Delete</button>
    {/if}
    <span class="mr-4">Likes: {likeCount}</span>
    <span>Comments: {commentCount}</span>
  </div>
</div>

<style>
  .post-big {
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 3%;
    color: black;
    font-size: large;

    width: 600px;
  }
  .post-mid {
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 3%;
    color: black;
    font-size: large;

    width: 70%;
  }
  .post-small {
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 3%;
    color: black;
    font-size: large;

    width: 450px;
  }
  .post-header {
    display: flex;
    flex-direction: column;
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
  .shared-post {
    border: 25px;
    border-color: #008480;
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
