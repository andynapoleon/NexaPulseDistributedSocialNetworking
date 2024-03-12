<script>
  import CreatePost from "../../widgets/CreatePost.svelte";
  import Post from "../../widgets/Post.svelte";
  import { onMount, beforeUpdate } from "svelte";
  import {
    authToken,
    isLoginPage,
    getCurrentUser,
    currentUser,
    server,
  } from "../../stores/stores.js";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";
  import { get } from "svelte/store";

  export let params;
  let postId = params.id;
  let post;
  let comments = [];
  let error = false;

  let authorId = $currentUser.userId;
  let commentText = ""; // Variable to hold the new comment text

  let commentCount;
  let likeCount;

  async function fetchPostById() {
    console.log("fetching post by ID");
    try {
      const response = await fetch(`${server}/api/posts/${postId}`);
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        post = data;
        fetchComments(); // Fetch comments after fetching the post
      } else {
        console.error("Failed to fetch post:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching post:", error.message);
    }
  }

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
        comments = await response.json();
        commentCount = comments.length;
      } else {
        console.error("Failed to fetch comments:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching comments:", error.message);
    }
  }

  // Function to add a comment
  async function addComment() {
    const addCommentEndpoint =
      server + `/api/authors/${authorId}/posts/${postId}/comments`;
    const response = await fetchWithRefresh(addCommentEndpoint, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${get(authToken)}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: 'comment',
        content_type: 'text/plain',
        comment: commentText,
        author: authorId,
        post: postId,
      }),
    });

    if (response.ok) {
      fetchComments();
      commentText = ''; // Clear the comment text after adding
    } else {
      console.error("Failed to add a comment:", response.statusText);
    }
  }

  async function sendLikeNotification() {
    try {
      const sendLikeEndpoint =
        server + `/api/authors/${authorId}/inbox`;
      const response = await fetch(sendLikeEndpoint, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${get(authToken)}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          postId: postId,
          authorId: authorId,
        }),
      });
      if (response.ok) {
        console.log("Like notification sent successfully");
      } else {
        console.error("Failed to send like notification:", response.statusText);
      }
    } catch (error) {
      console.error("Error sending like notification:", error.message);
    }
  }

  async function likePost() {
    // Perform like action
    // Update likeCount
    // Call sendLikeNotification
  }

  onMount(fetchPostById);
  
</script>

<main class="posts">
  {#if post}
    <Post {post} bind:commentCount bind:likeCount on:like={likePost}></Post>
    <h2>Comments:</h2>
    {#if comments.length > 0}
      <ul class="comment-list">
        {#each comments as comment}
          <li class="comment">{comment.comment}</li>
        {/each}
      </ul>
    {:else}
      <p>No comments yet</p>
    {/if}
    
    <!-- Box to add new comment -->
    <div class="new-comment-box">
      <textarea bind:value={commentText} placeholder="Add your comment"></textarea>
      <button on:click={addComment}>Add Comment</button>
    </div>
  {:else}
    <p>Loading post...</p>
  {/if}
</main>

<style>
  .posts {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }
  
  .comment-list {
    list-style-type: none; /* Remove default bullet points */
    padding: 0;
  }

  .comment {
    color: black; /* Set text color to black */
    margin-bottom: 10px; /* Add some spacing between comments */
  }

  p, h2 {
    color: black;
  }
  
  .new-comment-box {
    margin-top: 20px;
  }
  
  .new-comment-box textarea {
    width: 100%;
    height: 100px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-bottom: 10px;
    resize: none;
    /* Ensure cursor is visible */
    color: black;
    caret-color: black;
  }
  
  .new-comment-box button {
    background-color: #008080;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
</style>