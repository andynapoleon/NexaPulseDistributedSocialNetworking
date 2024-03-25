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
  let contentType = "text/plain"; // or text/markdown
  let files, input;
  export let streamType;
  const dispatch = createEventDispatcher();

  let id = $currentUser.userId;

  // Function to handle form submission
  export async function submitPost() {
    // if (postContent.trim() === "") {
    //   // Prevent submission of empty content
    //   console.error("Post content cannot be empty");
    //   return;
    // }
  
    let imageData = "";
    if (files) {
      imageData = await readFileAsBase64(files[0]);
    }

    const postData = {
      authorId: id,
      type: "post",
      title: postTitle,
      content: postContent,
      contentType: contentType,
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
  // Function to handle cancel action
  function removeInputFile() {
    files = null;
    input.value = '';
    visibility = "Public";
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
  <div class="file-input-container">
    <input type="file" bind:files bind:this={input} class="post-image" accept="image/png, image/jpeg" />
    {#if files}
      <button class="remove-file-button" on:click={removeInputFile}>Remove</button>
    {/if}
  </div>
  <div class="select-container">
    <select class="visibility-select" bind:value={visibility}>
      <option value="Public">Public</option>
      <option value="Unlisted">Unlisted</option>
      <option value="Friends">Friends</option>
    </select>
    <select class="format-select" bind:value={contentType}>
      <option value="text/plain">Normal</option>
      <option value="text/markdown">CommonMark</option>
    </select>
  </div>
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
  .file-input-container {
    display: flex; /* Use flexbox to align elements */
    align-items: center; /* Align elements vertically */
    margin-bottom: 5px; /* Adjust margin as needed */
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
  .format-select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-color: gray;
    border: 1px solid #ccc;
    padding: 8px;
    border-radius: 4px;
    width: 10%;
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
  .remove-file-button {
    padding: 7px 12px;
    border: 1px solid #ccc;
    background-color: white;
    /* border-radius: 4px; */
    /* background-color: teal; */
    font-weight:550;
    color: rgb(176, 3, 3);
    width: auto; /* Allow the button to adjust its width based on content */
    margin-top: 0;
    margin-left: 5px; /* Move the button to the right */
    cursor: pointer; /* Show pointer cursor when hovering over the button */
  }
  .select-container {
  display: flex;
  }

  .select-container select {
    margin-right: 10px; /* Adjust spacing between selects as needed */
  }
</style>
