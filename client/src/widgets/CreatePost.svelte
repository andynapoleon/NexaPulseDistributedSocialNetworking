<script>
  import { authToken, server } from "../stores/stores.js";
  import { currentUser } from "../stores/stores.js";
  import { get } from "svelte/store";
  import { fetchWithRefresh } from "../utils/apiUtils.js";
  import { posts } from "../stores/stores.js";
  import { createEventDispatcher } from "svelte";

  let postTitle = "";
  let postContent = "";
  let visibility = "Public";
  let content_type = "text/markdown";
  let files, input;
  export let streamType;
  const dispatch = createEventDispatcher();

  let id = $currentUser.userId;

  // Function to handle form submission
  export async function submitPost() {
    if (postContent.trim() === "") {
      // Prevent submission of empty content
      console.error("Post content cannot be empty");
      return;
    }
  
    let imageData = "";
    if (files) {
      imageData = await readFileAsBase64(files[0]);
    }

    const postData = {
      authorId: id,
      type: "post",
      title: postTitle,
      content: postContent,
      content_type: content_type,
      visibility: visibility.toUpperCase(),
      image: imageData,
    };

    console.log("Data to be sent:", postData);

    try {
      const response = await fetchWithRefresh(
        server + `/api/authors/${id}/posts/`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${get(authToken)}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(postData),
        }
      );

      if (response.ok) {
        console.log("Post created successfully!");
        dispatch("submit", { currentStream: streamType });
        // Reset input fields after successful submission
        postContent = "";
        postTitle = "";
        input.value = ''
        visibility = "Public";
      } else {
        console.error("Failed to create post");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  // Function to read image file as base64
  function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        resolve(reader.result);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
</script>

<div class="create-post">
  <input
    type="text"
    class="post-title"
    placeholder="Title"
    bind:value={postTitle}
  />
  <textarea
    class="post-content"
    placeholder="What's on your mind?"
    bind:value={postContent}
  ></textarea>
  <input type="file" bind:files bind:this={input} class="post-image" accept="image/png, image/jpeg" />
  <select class="visibility-select" bind:value={visibility}>
    <option value="Public">Public</option>
    <option value="Unlisted">Unlisted</option>
    <option value="Friends">Friends</option>
  </select>
  <button class="post-button" on:click={submitPost}>Post</button>
</div>

<style>
  .create-post {
    display: flex;
    flex-direction: column;
    justify-content: right;
    margin-bottom: 20px;
  }
  .post-title,
  .post-content,
  .post-image {
    color: black;
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  .visibility-select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-color: gray;
    border: 1px solid #ccc;
    padding: 8px;
    border-radius: 4px;
    width: 7%;
    font-size: 16px;
    margin-bottom: 0;
    margin-top: 0;
    text-align: center;
  }
  button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background-color: teal;
    color: white;
    font-weight: bold;
    width: 7%;
    margin-left: 93%;
  }
</style>
